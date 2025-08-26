# Django Job Portal

A modern job portal platform built with Django, featuring a clean UI and comprehensive job management system.

![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0-38B2AC.svg)

## 🚀 Features

### For Job Seekers
- 🔍 Advanced job search with filters
- 📝 Easy job application process
- 📱 Responsive mobile-friendly interface
- 📋 Track application status
- 💼 Resume upload functionality

### For Employers
- ✨ Post and manage job listings
- 👥 Review applications
- 📊 Application tracking dashboard
- 🔄 Update job status
- 📈 Basic analytics for job posts

### General Features
- 🎨 Modern, responsive UI with Tailwind CSS
- 🔐 User authentication system
- 🎭 Role-based access control (Employer/Job Seeker)
- 📱 Mobile-friendly design
- ⚡ Real-time search functionality
- 📄 Pagination for job listings

## 🛠️ Technology Stack

- **Backend:** Django 5.2.5
- **Frontend:** 
  - HTML5
  - Tailwind CSS
  - JavaScript
- **Database:** SQLite3 (default)
- **Authentication:** Django Authentication System

## 📋 Prerequisites

- Python 3.13+
- pip (Python package manager)
- Virtual environment (recommended)

## ⚙️ Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/jobportal.git
cd jobportal
```

2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables (if any)
```bash
# Create .env file in root directory
SECRET_KEY=your_secret_key
DEBUG=True
```

5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application in action.

## 📁 Project Structure

```
jobportal/
├── jobportal/          # Project settings directory
├── jobs/              # Main application directory
│   ├── migrations/    # Database migrations
│   ├── templates/     # HTML templates
│   ├── static/       # Static files (CSS, JS, images)
│   ├── models.py     # Database models
│   ├── views.py      # View logic
│   ├── forms.py      # Form definitions
│   └── urls.py       # URL configurations
├── media/            # User-uploaded files
├── static/           # Project-wide static files
├── manage.py         # Django management script
└── requirements.txt  # Project dependencies
```

## 🔑 Key Models

### User Model
- Custom user model extending Django's AbstractUser
- Supports both employer and job seeker roles

### Job Model
- Title, company name, location
- Job type (Full-time, Part-time, etc.)
- Salary information
- Job description and requirements
- Benefits and other details

### Application Model
- Links job seekers to jobs
- Includes resume and cover letter
- Tracks application status

## 💡 Usage

### For Employers
1. Register as an employer
2. Post new job listings
3. Review applications
4. Update application status
5. Manage job posts

### For Job Seekers
1. Register as a job seeker
2. Browse available jobs
3. Apply with resume and cover letter
4. Track application status
5. Search and filter jobs

## 🔒 Security Features

- CSRF protection
- Secure password hashing
- Role-based access control
- Form validation
- Secure file upload handling

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)
*Description: The main landing page showing featured job listings and search functionality.*

### Job Listings
![Job Listings](screenshots/job-listings.png)
*Description: Grid view of all available jobs with filtering options.*

### Job Details
![Job Details](screenshots/job-details.png)
*Description: Detailed view of a job posting with all information and apply button.*

### Application Dashboard
![Application Dashboard](screenshots/dashboard.png)
*Description: User dashboard showing application status and history.*

### Post Job Form
![Post Job](screenshots/post-job.png)
*Description: Form for employers to create new job listings.*

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Abir Hasan

## 🙏 Acknowledgments

- Django documentation
- Tailwind CSS team
- Open source community

