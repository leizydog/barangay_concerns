# apps/notifications/models.py
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Model to store user notifications for concern updates.
    """
    NOTIFICATION_TYPES = (
        ('STATUS_CHANGE', 'Status Changed'),
        ('PRIORITY_CHANGE', 'Priority Changed'),
        ('COMMENT', 'New Comment'),
        ('ASSIGNED', 'Concern Assigned'),
        ('RESOLVED', 'Concern Resolved'),
        ('ARCHIVED', 'Concern Archived'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    concern = models.ForeignKey(
        'concerns.Concern',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='STATUS_CHANGE'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.title} - {'Read' if self.is_read else 'Unread'}"

    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    @classmethod
    def get_unread_count(cls, user):
        """Get the count of unread notifications for a user."""
        return cls.objects.filter(user=user, is_read=False).count()

    @classmethod
    def mark_all_as_read(cls, user):
        """Mark all notifications as read for a user."""
        cls.objects.filter(user=user, is_read=False).update(is_read=True)
