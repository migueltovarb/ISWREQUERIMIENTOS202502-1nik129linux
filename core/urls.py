from django.urls import path
from django.contrib.auth import views as auth_views # Import this!
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    # Login & Logout (Using Django's built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # The Main App Features
    path('dashboard/', views.patient_dashboard, name='dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    # NEW: Doctor Paths
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('update-appointment/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('edit-appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
]