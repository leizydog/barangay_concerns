from django.urls import path
from . import views

# Change app_name from 'accounts' to 'security_management'
app_name = 'security_management' 

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    
    # Admin Routes
    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('admin/users/<int:user_id>/action/', views.admin_user_action_view, name='admin_user_action'),
    path('admin/announcements/', views.admin_announcements_view, name='admin_announcements'),
    path('admin/reports/', views.admin_reports_view, name='admin_reports'),
    path('admin/reports/<int:report_id>/action/', views.admin_report_action_view, name='admin_report_action'),
]