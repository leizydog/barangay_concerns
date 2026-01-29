from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('LGU', 'LGU Staff'),
        ('ADMIN', 'System Admin'),
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
    
    # Legal Action / Trolling Prevention
    is_flagged_for_legal_action = models.BooleanField(default=False, help_text="Flagged by LGU for legal action due to trolling/misconduct")
    legal_action_reason = models.TextField(blank=True, help_text="Reason for legal action")
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_lgu(self):
        return self.role in ['LGU', 'ADMIN']
        
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def is_regular_user(self):
        return self.role == 'USER'

class Announcement(models.Model):
    TYPES = (
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('DANGER', 'Emergency/Danger'),
        ('SUCCESS', 'Good News'),
    )
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPES, default='INFO')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    active_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.get_type_display()}] {self.message[:50]}"
    
    @property
    def is_currently_active(self):
        """Check if announcement is both flagged active AND not expired."""
        if not self.is_active:
            return False
        if self.active_until and self.active_until < timezone.now():
            return False
        return True

class AuditLog(models.Model):
    ACTIONS = (
        ('BAN', 'Banned User'),
        ('UNBAN', 'Unbanned User'),
        ('PROMOTE', 'Promoted Role'),
        ('DEMOTE', 'Demoted Role'),
        ('RESET_KARMA', 'Reset Karma'),
        ('DELETE_REPORT', 'Deleted Report'),
        ('ANNOUNCEMENT', 'Created Announcement'),
    )
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_actions')
    action = models.CharField(max_length=20, choices=ACTIONS)
    target = models.CharField(max_length=255, help_text="Username or Object ID")
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor} - {self.action} - {self.target}"