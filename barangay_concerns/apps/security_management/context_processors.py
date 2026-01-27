from django.utils import timezone
from .models import Announcement

def active_announcements(request):
    """
    Inject active global announcements into the template context.
    """
    now = timezone.now()
    announcements = Announcement.objects.filter(
        is_active=True, 
        active_until__gte=now
    ).order_by('-created_at')
    
    return {'global_announcements': announcements}
