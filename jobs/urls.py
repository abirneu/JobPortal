from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='home'),
    path('jobs/', views.job_list, name='job_list'),  # Added this line
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/applications/', views.manage_applications, name='manage_applications'),
    path('applications/<int:application_id>/status/', views.update_application_status, name='update_application_status'),


]