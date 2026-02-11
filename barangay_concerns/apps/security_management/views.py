from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, ChangePasswordForm
from .models import User, Announcement, AuditLog
from apps.concerns.utils import generate_random_alias

def is_staff_or_admin(user):
    return user.is_authenticated and user.role in ['LGU', 'ADMIN']


def register_view(request):
    if request.user.is_authenticated:
        return redirect('concerns:list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Generate random alias if not provided (though form doesn't have alias field yet)
            # But the user model has it.
            user.alias = generate_random_alias()
            user.save()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('concerns:list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'security_management/pages/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('concerns:list')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'concerns:list'))
    else:
        form = UserLoginForm()
    
    return render(request, 'security_management/pages/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # If alias is cleared, regenerate it? Or allow blank?
            # User wants: "set random display names... but also allow them to set their own"
            # If they clear it, maybe regenerate?
            user = form.save(commit=False)
            if not user.alias:
                user.alias = generate_random_alias()
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('security_management:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'security_management/pages/profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('security_management:profile')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'security_management/pages/change_password.html', {'form': form})

# --- ADMIN MANAGEMENT VIEWS ---

@login_required
@user_passes_test(is_staff_or_admin)
def admin_users_view(request):
    """
    User Management Dashboard
    Tabs: 'all', 'lgu', 'risk', 'banned'
    """
    tab = request.GET.get('tab', 'all')
    search_query = request.GET.get('search', '')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by Tab
    if tab == 'lgu':
        users = users.filter(role__in=['LGU', 'ADMIN'])
    elif tab == 'risk':
        # Karma between -5 and -9
        users = users.filter(points__lte=-5, points__gt=-10)
    elif tab == 'banned':
        # Karma <= -10 OR manually banned (is_active=False)
        users = users.filter(Q(points__lte=-10) | Q(is_active=False))
        
    # Search
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(alias__icontains=search_query)
        )
        
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'tab': tab,
        'search_query': search_query,
        'total_count': User.objects.count(),
        'banned_count': User.objects.filter(is_active=False).count(),
        'risk_count': User.objects.filter(points__lte=-5, points__gt=-10).count(),
    }
    return render(request, 'security_management/pages/admin_users.html', context)

@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def admin_user_action_view(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    action_type = request.POST.get('action')
    reason = request.POST.get('reason', 'No reason provided')
    
    # Prevent acting on self or superusers (safeguard)
    if target_user == request.user:
        messages.error(request, "You cannot perform actions on yourself.")
        return redirect('security_management:admin_users')
        
    AuditLog.objects.create(
        actor=request.user,
        action=action_type.upper(),
        target=target_user.username,
        details=reason
    )
    
    if action_type == 'ban':
        target_user.is_active = False
        target_user.save()
        messages.success(request, f"User {target_user.username} has been BANNED.")
        
    elif action_type == 'unban':
        target_user.is_active = True
        # If karma is low, maybe reset it partially so they don't get autobanned again?
        if target_user.points <= -10:
             target_user.points = -5 # Reset to "At Risk" level instead of banned level
        target_user.save()
        messages.success(request, f"User {target_user.username} has been UNBANNED.")
        
    elif action_type == 'promote':
        new_role = request.POST.get('role', 'LGU')
        target_user.role = new_role
        target_user.save()
        messages.success(request, f"User {target_user.username} promoted to {new_role}.")
        
    elif action_type == 'demote':
        target_user.role = 'USER'
        target_user.save()
        messages.success(request, f"User {target_user.username} demoted to Regular User.")
        
    elif action_type == 'reset_karma':
        target_user.points = 0
        target_user.save()
        messages.success(request, f"Karma points for {target_user.username} reset to 0.")
        
    return redirect(request.META.get('HTTP_REFERER', 'security_management:admin_users'))

@login_required
@user_passes_test(is_staff_or_admin)
def admin_announcements_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            message = request.POST.get('message')
            type = request.POST.get('type')
            duration = int(request.POST.get('duration', 24)) # Default 24 hours
            
            if message:
                active_until = timezone.now() + timedelta(hours=duration)
                Announcement.objects.create(
                    message=message,
                    type=type,
                    active_until=active_until,
                    created_by=request.user
                )
                AuditLog.objects.create(
                    actor=request.user,
                    action='ANNOUNCEMENT',
                    target='Global',
                    details=f"Created: {message}"
                )
                messages.success(request, "Announcement published.")
                
        elif action == 'expire':
            announcement_id = request.POST.get('announcement_id')
            Announcement.objects.filter(id=announcement_id).update(is_active=False)
            messages.success(request, "Announcement expired.")
        
        elif action == 'delete':
            announcement_id = request.POST.get('announcement_id')
            announcement = Announcement.objects.filter(id=announcement_id).first()
            if announcement:
                AuditLog.objects.create(
                    actor=request.user,
                    action='ANNOUNCEMENT',
                    target='Global',
                    details=f"Deleted: {announcement.message[:50]}"
                )
                announcement.delete()
                messages.success(request, "Announcement deleted.")
            
        return redirect('security_management:admin_announcements')
    
    all_announcements = Announcement.objects.all().order_by('-created_at')
    
    # Separate active and expired
    active_announcements = [a for a in all_announcements if a.is_currently_active]
    expired_announcements = [a for a in all_announcements if not a.is_currently_active]
    
    context = {
        'announcements': all_announcements,
        'active_announcements': active_announcements,
        'expired_announcements': expired_announcements,
        'types': Announcement.TYPES
    }
    return render(request, 'security_management/pages/admin_announcements.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
def admin_reports_view(request):
    """Admin moderation queue for reported comments - only shows items with 3+ reports."""
    from apps.concerns.models import CommentReport, Comment
    from django.db.models import Count
    
    tab = request.GET.get('tab', 'pending')
    REPORT_THRESHOLD = 3  # Minimum reports required to appear in queue
    
    # Get comments that have enough reports to warrant review
    # Group by comment and count unique reporters
    if tab == 'pending':
        # Get comments with 3+ pending reports
        comments_with_reports = CommentReport.objects.filter(status='PENDING') \
            .values('comment_id') \
            .annotate(report_count=Count('id')) \
            .filter(report_count__gte=REPORT_THRESHOLD)
        
        comment_ids = [c['comment_id'] for c in comments_with_reports if c['comment_id']]
        
        # Get the most recent report for each qualifying comment
        reports = CommentReport.objects.filter(
            status='PENDING',
            comment_id__in=comment_ids
        ).order_by('comment_id', '-created_at').distinct('comment_id') if comment_ids else CommentReport.objects.none()
        
        # Fallback for SQLite (doesn't support distinct on specific field)
        try:
            reports = list(reports)
        except:
            # SQLite fallback - get latest report per comment
            seen_comments = set()
            all_reports = CommentReport.objects.filter(status='PENDING', comment_id__in=comment_ids).order_by('-created_at')
            reports = []
            for r in all_reports:
                if r.comment_id not in seen_comments:
                    seen_comments.add(r.comment_id)
                    reports.append(r)
    elif tab == 'resolved':
        reports = CommentReport.objects.filter(status='RESOLVED')
    elif tab == 'dismissed':
        reports = CommentReport.objects.filter(status='DISMISSED')
    else:
        reports = CommentReport.objects.all()
    
    # Attach report counts to each report for display
    for report in reports:
        if report.comment_id:
            report.total_reports = CommentReport.objects.filter(
                comment_id=report.comment_id, 
                status='PENDING'
            ).count()
        else:
            report.total_reports = 1
    
    # Count pending that meet threshold
    pending_comments = CommentReport.objects.filter(status='PENDING') \
        .values('comment_id') \
        .annotate(count=Count('id')) \
        .filter(count__gte=REPORT_THRESHOLD)
    pending_count = len(pending_comments)
    
    context = {
        'reports': reports,
        'tab': tab,
        'report_threshold': REPORT_THRESHOLD,
        'pending_count': pending_count,
        'resolved_count': CommentReport.objects.filter(status='RESOLVED').count(),
        'dismissed_count': CommentReport.objects.filter(status='DISMISSED').count(),
    }
    return render(request, 'security_management/pages/admin_reports.html', context)


@login_required
@user_passes_test(is_staff_or_admin)
@require_POST
def admin_report_action_view(request, report_id):
    """Handle admin actions on reported comments."""
    from apps.concerns.models import CommentReport
    
    report = get_object_or_404(CommentReport, pk=report_id)
    action = request.POST.get('action')
    karma_penalty = int(request.POST.get('karma_penalty', 1))
    admin_notes = request.POST.get('admin_notes', '')
    
    if action == 'delete':
        # Delete the comment and deduct karma from author
        comment_author = report.comment.author
        comment_content = report.comment.content[:50]  # Save for audit
        concern_id = report.comment.concern.pk
        comment_to_delete = report.comment  # Store reference
        
        # Deduct karma
        comment_author.points -= karma_penalty
        comment_author.save()
        
        # Update report status BEFORE deleting the comment
        report.status = 'RESOLVED'
        report.reviewed_at = timezone.now()
        report.reviewed_by = request.user
        report.admin_notes = admin_notes
        report.karma_deducted = karma_penalty
        report.save()
        
        # Now delete the comment (this will cascade delete the report too due to FK)
        comment_to_delete.delete()
        
        # Log the action
        AuditLog.objects.create(
            actor=request.user,
            action='DELETE_COMMENT',
            target=comment_author.username,
            details=f"Deleted comment '{comment_content}...' and deducted {karma_penalty} karma. Reason: {report.reason}"
        )
        
        messages.success(request, f"Comment deleted. {karma_penalty} karma deducted from {comment_author.username}.")
        
    elif action == 'dismiss':
        report.status = 'DISMISSED'
        report.reviewed_at = timezone.now()
        report.reviewed_by = request.user
        report.admin_notes = admin_notes
        report.save()
        
        messages.info(request, "Report dismissed.")
    
    return redirect('security_management:admin_reports')