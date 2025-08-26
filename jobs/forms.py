from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Job, Application
import os

class UserRegisterForm(UserCreationForm):
    is_employer = forms.BooleanField(
        required=False,
        label='Register as Employer',
        widget=forms.RadioSelect(choices=[(True, 'Employer'), (False, 'Applicant')])

        
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_employer']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'job_type', 'salary', 'description', 'requirements', 'benefits']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 py-3 pl-3 ',
                'placeholder': 'px-2 e.g., Senior Software Engineer'
            }),
            'company_name': forms.TextInput(attrs={ 
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 py-3 pl-3',
                'placeholder': 'e.g., Tech Solutions Inc.'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 py-3 pl-3',
                'placeholder': 'e.g., New York, NY or Remote'
            }),
            'job_type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 py-3 pl-3'
            }),
            'salary': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 py-3 pl-3',
                'placeholder': 'e.g., 80,000 - 120,000/month'
            }),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 pl-3 ',
                'placeholder': 'Describe the role, responsibilities, and expectations...'
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 pl-3',
                'placeholder': 'List required skills, experience, education...'
            }),
            'benefits': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200 pl-3',
                'placeholder': 'List benefits, perks, and other offerings...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields except title required=False to allow partial updates
        for field_name, field in self.fields.items():
            if field_name != 'title':
                field.required = False

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 5,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-violet-500 focus:ring-violet-500 sm:text-sm transition duration-200',
                'placeholder': 'Tell us why you would be a great fit for this position...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'sr-only',
                'accept': '.pdf,.doc,.docx'
            })
        }
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Validate file extension
            valid_extensions = ['.pdf', '.doc', '.docx']
            ext = os.path.splitext(resume.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    'Unsupported file format. Please upload PDF or Word documents only.'
                )
            
            # Validate file size (5MB limit)
            max_size = 5 * 1024 * 1024  # 5MB
            if resume.size > max_size:
                raise forms.ValidationError(
                    'File size exceeds the 5MB limit. Please upload a smaller file.'
                )
        else:
            raise forms.ValidationError('Resume is required.')
        return resume

    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        if len(cover_letter) < 50:
            raise forms.ValidationError(
                'Cover letter should be at least 50 characters long.'
            )
        return cover_letter