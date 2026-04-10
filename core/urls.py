from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/complaint/submit/', views.submit_complaint, name='submit_complaint'),
    path('student/complaint/edit/<int:pk>/', views.edit_complaint, name='edit_complaint'),
    path('student/complaint/delete/<int:pk>/', views.delete_complaint, name='delete_complaint'),
    
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/complaint/update/<int:pk>/', views.update_complaint_status, name='update_complaint_status'),
    path('admin/leaderboard/', views.admin_leaderboard, name='leaderboard'),
    path('admin/analytics/', views.complaint_analytics, name='analytics'),
]
