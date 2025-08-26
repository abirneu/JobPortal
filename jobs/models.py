from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=True)

    def __str__(self):
        return self.username
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
    ]
    
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    salary = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE,
        related_name='applications'  # Added related_name
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Changed from User to settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='job_applications'  # Added related_name
    )
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title} (Status: {self.get_status_display()})"