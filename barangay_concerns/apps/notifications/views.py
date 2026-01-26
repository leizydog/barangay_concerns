# apps/notifications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification


@login_required
def notification_list_view(request):
    """
    Display all notifications for the current user.
    """
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)


@login_required
def notification_mark_read_view(request, pk):
    """
    Mark a single notification as read.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    
    # If there's a concern linked, redirect to it
    if notification.concern:
        return redirect('concerns:detail', pk=notification.concern.pk)
    
    return redirect('notifications:list')


@login_required
def notification_mark_all_read_view(request):
    """
    Mark all notifications as read for the current user.
    """
    if request.method == 'POST':
        Notification.mark_all_as_read(request.user)
        messages.success(request, 'All notifications marked as read.')
    
    return redirect('notifications:list')


@login_required
def notification_delete_view(request, pk):
    """
    Delete a single notification.
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    if request.method == 'POST':
        notification.delete()
        messages.success(request, 'Notification deleted.')
    
    return redirect('notifications:list')


@login_required
def notification_delete_all_read_view(request):
    """
    Delete all read notifications for the current user.
    """
    if request.method == 'POST':
        deleted_count = Notification.objects.filter(
            user=request.user,
            is_read=True
        ).delete()[0]
        messages.success(request, f'Deleted {deleted_count} read notifications.')
    
    return redirect('notifications:list')


@login_required
def notification_count_api(request):
    """
    API endpoint to get the unread notification count.
    Used for updating the navbar badge dynamically.
    """
    count = Notification.get_unread_count(request.user)
    return JsonResponse({'count': count})
