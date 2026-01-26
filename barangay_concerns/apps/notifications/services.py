# apps/notifications/services.py
"""
Service functions for creating and sending notifications.
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification


def create_notification(user, concern, notification_type, title, message):
    """
    Create a notification for a user.
    
    Args:
        user: The user to notify
        concern: The related concern
        notification_type: Type of notification (STATUS_CHANGE, COMMENT, etc.)
        title: Notification title
        message: Notification message
    
    Returns:
        The created Notification object
    """
    notification = Notification.objects.create(
        user=user,
        concern=concern,
        notification_type=notification_type,
        title=title,
        message=message
    )
    
    # Send email notification if user has email
    if user.email:
        send_email_notification(user, notification)
    
    return notification


def send_email_notification(user, notification):
    """
    Send an email notification to the user.
    
    Args:
        user: The user to send email to
        notification: The notification object with details
    """
    try:
        subject = f"🔔 {notification.title}"
        
        # Plain text version
        plain_message = f"""
Hello {user.get_full_name() or user.username},

{notification.message}

Concern: {notification.concern.title}
Status: {notification.concern.get_status_display()}

View details at: /concerns/{notification.concern.pk}/

---
Barangay Concerns Platform
        """
        
        # HTML version
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb;">🔔 {notification.title}</h2>
                <p>{notification.message}</p>
                
                <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Concern:</strong> {notification.concern.title}</p>
                    <p><strong>Status:</strong> {notification.concern.get_status_display()}</p>
                    <p><strong>Category:</strong> {notification.concern.get_category_display()}</p>
                </div>
                
                <a href="/concerns/{notification.concern.pk}/" 
                   style="display: inline-block; background: #2563eb; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 8px; font-weight: bold;">
                    View Details
                </a>
                
                <hr style="margin-top: 30px; border: none; border-top: 1px solid #e2e8f0;">
                <p style="color: #64748b; font-size: 12px;">
                    Barangay Concerns Platform - Helping build better communities
                </p>
            </div>
        </body>
        </html>
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@barangay-concerns.local',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True  # Don't crash if email fails
        )
    except Exception as e:
        # Log the error but don't crash
        print(f"Failed to send email notification: {e}")


def notify_status_change(concern, old_status, new_status, changed_by=None):
    """
    Create a notification when a concern's status changes.
    
    Args:
        concern: The concern that was updated
        old_status: Previous status
        new_status: New status
        changed_by: User who made the change (optional)
    """
    # Notify the reporter
    if concern.reporter:
        status_emojis = {
            'PENDING': '⏳',
            'IN_PROGRESS': '🔄',
            'RESOLVED': '✅',
            'CLOSED': '🔒'
        }
        
        emoji = status_emojis.get(new_status, '📢')
        old_display = dict(concern.STATUS_CHOICES).get(old_status, old_status)
        new_display = dict(concern.STATUS_CHOICES).get(new_status, new_status)
        
        title = f"{emoji} Your concern status updated to {new_display}"
        message = f"Your reported concern \"{concern.title}\" has been updated from {old_display} to {new_display}."
        
        if changed_by:
            message += f" Updated by {changed_by.get_full_name() or changed_by.username}."
        
        create_notification(
            user=concern.reporter,
            concern=concern,
            notification_type='STATUS_CHANGE',
            title=title,
            message=message
        )


def notify_priority_change(concern, old_priority, new_priority, changed_by=None):
    """
    Create a notification when a concern's priority changes.
    """
    if concern.reporter:
        priority_emojis = {
            'LOW': '🟢',
            'MEDIUM': '🟡',
            'HIGH': '🟠',
            'URGENT': '🔴'
        }
        
        emoji = priority_emojis.get(new_priority, '📢')
        old_display = dict(concern.PRIORITY_CHOICES).get(old_priority, old_priority)
        new_display = dict(concern.PRIORITY_CHOICES).get(new_priority, new_priority)
        
        title = f"{emoji} Concern priority updated to {new_display}"
        message = f"The priority of your concern \"{concern.title}\" has been changed from {old_display} to {new_display}."
        
        create_notification(
            user=concern.reporter,
            concern=concern,
            notification_type='PRIORITY_CHANGE',
            title=title,
            message=message
        )


def notify_concern_resolved(concern):
    """
    Create a notification when a concern is resolved.
    """
    if concern.reporter:
        title = "✅ Your concern has been resolved!"
        message = f"Great news! Your reported concern \"{concern.title}\" has been marked as resolved. Thank you for helping improve our community!"
        
        create_notification(
            user=concern.reporter,
            concern=concern,
            notification_type='RESOLVED',
            title=title,
            message=message
        )


def notify_concern_archived(concern):
    """
    Create a notification when a concern is archived.
    """
    if concern.reporter:
        title = "📦 Your concern has been archived"
        message = f"Your concern \"{concern.title}\" has been archived by LGU staff."
        
        create_notification(
            user=concern.reporter,
            concern=concern,
            notification_type='ARCHIVED',
            title=title,
            message=message
        )
