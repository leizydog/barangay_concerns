from django.urls import path
from . import views

# Change app_name from 'accounts' to 'security_management'
app_name = 'security_management' 

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # ... any other URLs
]