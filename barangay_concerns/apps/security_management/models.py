from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('LGU', 'LGU Staff'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    phone_number = models.CharField(max_length=15, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    municipality = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    # Geographic Profile
    region = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True, help_text="City or Municipality")
    
    # Gamification & Identity
    alias = models.CharField(max_length=50, blank=True, null=True, unique=True, help_text="Public display name")
    points = models.IntegerField(default=0, help_text="Karma points")
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_lgu(self):
        return self.role == 'LGU'
    
    def is_regular_user(self):
        return self.role == 'USER'