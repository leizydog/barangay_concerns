# apps/notifications/signals.py
"""
Django signals to automatically create notifications when concerns are updated.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.concerns.models import Concern
from . import services


# Store the old values before save
@receiver(pre_save, sender=Concern)
def concern_pre_save(sender, instance, **kwargs):
    """
    Store the old status and priority before the concern is saved.
    This allows us to compare and notify on changes.
    """
    if instance.pk:
        try:
            old_instance = Concern.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
            instance._old_priority = old_instance.priority
            instance._old_is_archived = old_instance.is_archived
        except Concern.DoesNotExist:
            instance._old_status = None
            instance._old_priority = None
            instance._old_is_archived = None
    else:
        instance._old_status = None
        instance._old_priority = None
        instance._old_is_archived = None


@receiver(post_save, sender=Concern)
def concern_post_save(sender, instance, created, **kwargs):
    """
    Create notifications after a concern is saved.
    """
    # Don't notify on new concern creation
    if created:
        return
    
    old_status = getattr(instance, '_old_status', None)
    old_priority = getattr(instance, '_old_priority', None)
    old_is_archived = getattr(instance, '_old_is_archived', None)
    
    # Status change notification
    if old_status and old_status != instance.status:
        # Special notification for resolved
        if instance.status == 'RESOLVED':
            services.notify_concern_resolved(instance)
        else:
            services.notify_status_change(
                concern=instance,
                old_status=old_status,
                new_status=instance.status
            )
    
    # Priority change notification
    if old_priority and old_priority != instance.priority:
        services.notify_priority_change(
            concern=instance,
            old_priority=old_priority,
            new_priority=instance.priority
        )
    
    # Archive notification
    if old_is_archived is False and instance.is_archived is True:
        services.notify_concern_archived(instance)
