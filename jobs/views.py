from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Job, Application, User
from .forms import JobForm, ApplicationForm, UserRegisterForm



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_applicant = not form.cleaned_data.get('is_employer')
            user.is_employer = form.cleaned_data.get('is_employer')
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'registration/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if request.user.is_employer:
        jobs = Job.objects.filter(posted_by=request.user)
        for job in jobs:
            job.application_count = job.applications.count()
            job.pending_count = job.applications.filter(status='pending').count()
            job.approved_count = job.applications.filter(status='approved').count()
            job.rejected_count = job.applications.filter(status='rejected').count()
        return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})
    else:
        status_filter = request.GET.get('status', '')
        applications = Application.objects.filter(applicant=request.user)
        if status_filter and status_filter != 'all':
            applications = applications.filter(status=status_filter)
        return render(request, 'jobs/applicant_dashboard.html', {'applications': applications})


@login_required
def post_job(request):
    if not request.user.is_employer:
        return redirect('dashboard')
    
    # Check if we're editing an existing job
    job_id = request.GET.get('edit')
    job = None
    if job_id:
        job = get_object_or_404(Job, pk=job_id, posted_by=request.user)
    
    if request.method == 'POST':
        if job:
            # Editing existing job
            form = JobForm(request.POST, instance=job)
        else:
            # Creating new job
            form = JobForm(request.POST)
        
        if form.is_valid():
            job = form.save(commit=False)
            if not job.id:  # Only set posted_by for new jobs
                job.posted_by = request.user
            job.save()
            messages.success(request, 'Job updated successfully!' if job_id else 'Job posted successfully!')
            return redirect('dashboard')
    else:
        if job:
            # Pre-fill form with existing job data
            form = JobForm(instance=job)
        else:
            # Empty form for new job
            form = JobForm()
    
    return render(request, 'jobs/post_job.html', {
        'form': form,
        'job': job  # Pass the job object to the template
    })

from datetime import timedelta
from django.utils import timezone

def job_list(request):
    query = request.GET.get('q')
    page = request.GET.get('page', 1)
    
    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(location__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        jobs = Job.objects.all().order_by('-created_at')

    # Mark jobs as new if they were created in the last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    for job in jobs:
        job.is_new = job.created_at > seven_days_ago

    paginator = Paginator(jobs, 6)
    
    try:
        jobs_page = paginator.page(page)
    except PageNotAnInteger:
        jobs_page = paginator.page(1)
    except EmptyPage:
        jobs_page = paginator.page(paginator.num_pages)
    
    return render(request, 'jobs/job_list.html', {'jobs': jobs_page, 'query': query})

@login_required
def manage_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.user != job.posted_by:
        messages.error(request, "You don't have permission to view these applications.")
        return redirect('dashboard')
    
    applications = job.applications.all().order_by('-applied_at')
    return render(request, 'jobs/manage_applications.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    
    # Check if the user is the employer who posted the job
    if request.user != application.job.posted_by:
        messages.error(request, "You don't have permission to update this application.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            # Store old status for comparison
            old_status = application.status
            
            # Update the status
            application.status = new_status
            application.save()
            
            # Customize message based on the status
            status_messages = {
                'approved': 'Application approved successfully!',
                'rejected': 'Application rejected.',
                'pending': 'Application marked as pending.'
            }
            
            # Add success message for employer
            messages.success(request, status_messages.get(new_status, 'Status updated successfully.'))
            
            # If the status was changed from pending to approved/rejected
            if old_status == 'pending' and new_status in ['approved', 'rejected']:
                status_display = 'approved' if new_status == 'approved' else 'rejected'
                messages.info(
                    request,
                    f'The applicant will be notified that their application was {status_display}.'
                )
            
        else:
            messages.error(request, 'Invalid status value')
        
        # Always redirect back to manage applications page
        return redirect('manage_applications', job_id=application.job.id)
    
    # If not POST, redirect to dashboard
    return redirect('dashboard')
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    has_applied = Application.objects.filter(job=job, applicant=request.user).exists() if request.user.is_authenticated else False
    
    if request.method == 'POST' and request.user.is_applicant:
        if has_applied:
            messages.error(request, 'You have already applied for this position.')
            return redirect('job_list')
            
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard')
    else:
        form = ApplicationForm() if not has_applied else None
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'form': form,
        'has_applied': has_applied
    })

@login_required
def manage_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.user != job.posted_by:
        messages.error(request, "You don't have permission to view these applications.")
        return redirect('dashboard')
    
    # Get status filter from query params, default to 'all'
    status_filter = request.GET.get('status', 'all')
    
    # Start with all applications for this job
    applications = job.applications.all()
    
    # Apply status filter if specified
    if status_filter != 'all' and status_filter in dict(Application.STATUS_CHOICES):
        applications = applications.filter(status=status_filter)
    
    # Order applications: pending first, then most recent
    applications = applications.order_by(
        '-status',  # This will put pending applications first
        '-applied_at'  # Then sort by application date
    )
    
    # Count applications by status
    status_counts = {
        'total': job.applications.count(),
        'pending': job.applications.filter(status='pending').count(),
        'approved': job.applications.filter(status='approved').count(),
        'rejected': job.applications.filter(status='rejected').count(),
    }
    
    return render(request, 'jobs/manage_applications.html', {
        'job': job,
        'applications': applications,
        'status_counts': status_counts,
        'current_status': status_filter
    })



@login_required
def applicant_dashboard(request):
    status = request.GET.get('status', 'all')
    applications = Application.objects.filter(applicant=request.user)
    if status != 'all':
        applications = applications.filter(status=status)

    # Pass status options for template loop
    status_options = [
        ('all', 'All'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    return render(request, 'jobs/applicant_dashboard.html', {
        'applications': applications,
        'status_filter': status,
        'status_options': status_options,
    })
