# apps/concerns/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Concern(models.Model):
    CATEGORY_CHOICES = (
        ('FLOOD', 'Flooding'),
        ('ROAD', 'Road Infrastructure'),
        ('WASTE', 'Waste Management'),
        ('ELECTRICITY', 'Electricity'),
        ('WATER', 'Water Supply'),
        ('SAFETY', 'Public Safety'),
        ('OTHER', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    barangay = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    
    # Map coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    image = models.ImageField(upload_to='concerns/', blank=True, null=True)
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_concerns')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_concerns')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Archive and soft delete fields
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='archived_concerns')
    
    # Track if concern can be edited
    is_locked = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def get_category_icon(self):
        """Return emoji icon for category"""
        icons = {
            'FLOOD': '🌊',
            'ROAD': '🛣️',
            'WASTE': '🗑️',
            'ELECTRICITY': '⚡',
            'WATER': '💧',
            'SAFETY': '🚨',
            'OTHER': '📍',
        }
        return icons.get(self.category, '📍')
    
    def get_marker_color(self):
        """Return color based on status for map markers"""
        colors = {
            'PENDING': 'orange',
            'IN_PROGRESS': 'blue',
            'RESOLVED': 'green',
            'CLOSED': 'gray',
        }
        return colors.get(self.status, 'red')
    
    def can_be_edited(self):
        """Check if concern can be edited"""
        # Once in progress or beyond, it's locked for regular users
        return not self.is_locked and self.status == 'PENDING'
    
    def archive(self, user):
        """Archive the concern (soft delete)"""
        self.is_archived = True
        self.archived_at = timezone.now()
        self.archived_by = user
        self.save()
    
    def unarchive(self):
        """Unarchive the concern"""
        self.is_archived = False
        self.archived_at = None
        self.archived_by = None
        self.save()
    
    def save(self, *args, **kwargs):
        # Auto-lock when status changes from PENDING
        if self.pk:  # Only for existing objects
            old_concern = Concern.objects.filter(pk=self.pk).first()
            if old_concern and old_concern.status == 'PENDING' and self.status != 'PENDING':
                self.is_locked = True
        
        # Set resolved_at when status changes to RESOLVED or CLOSED
        if self.status in ['RESOLVED', 'CLOSED'] and not self.resolved_at:
            self.resolved_at = timezone.now()
        
        super().save(*args, **kwargs)