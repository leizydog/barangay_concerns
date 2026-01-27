# apps/concerns/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from .models import Concern, Comment, EmergencyUnit, Vote
from .forms import ConcernForm, ConcernUpdateForm, CommentForm
from .utils import generate_random_alias
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.notifications.services import notify_new_comment, notify_vote


def concern_list_view(request):
    # Exclude archived and closed concerns - show ALL to everyone
    concerns = Concern.objects.filter(is_archived=False).exclude(status='CLOSED')
    
    # Geographic Scope Filtering
    scope = request.GET.get('scope', 'national')
    
    # Only allow geo-filtering if user is logged in and has profile data
    user_location_set = False
    if request.user.is_authenticated:
        # Check if user has set their location
        if request.user.region and request.user.province:
            user_location_set = True
            
            if scope == 'regional':
                concerns = concerns.filter(region=request.user.region)
            elif scope == 'provincial':
                concerns = concerns.filter(province=request.user.province)
            elif scope == 'city':
                # Match either city field or municipality field
                city_val = request.user.city or request.user.municipality
                if city_val:
                    concerns = concerns.filter(municipality__icontains=city_val)
            elif scope == 'barangay':
                if request.user.barangay:
                    concerns = concerns.filter(barangay__icontains=request.user.barangay)
        else:
            # If user hasn't set location but tries to access local tabs, fallback to national
            if scope != 'national':
                pass # Or could add a message asking them to complete profile
                
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        concerns = concerns.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        concerns = concerns.filter(status=status_filter)
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        concerns = concerns.filter(category=category_filter)
    
    context = {
        'concerns': concerns,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'scope': scope,
        'user_location_set': user_location_set,
    }
    return render(request, 'concerns/list.html', context)

def concern_map_view(request):
    """Display all concerns on an interactive map - exclude closed and archived"""
    concerns = Concern.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False,
        is_archived=False
    ).exclude(status='CLOSED')
    
    # MAP SHOWS EVERYTHING - No User Filtering as requested ("map shows everything")
    
    # Apply same filters as list view
    status_filter = request.GET.get('status', '')
    if status_filter:
        concerns = concerns.filter(status=status_filter)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        concerns = concerns.filter(category=category_filter)
    
    context = {
        'concerns': concerns,
        'status_filter': status_filter,
        'category_filter': category_filter,
    }
    return render(request, 'concerns/map.html', context)

def concern_map_data(request):
    """API endpoint to get data for map - exclude closed and archived"""
    concerns = Concern.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False,
        is_archived=False
    ).exclude(status='CLOSED')
    
    # Apply filters
    status_filter = request.GET.get('status', '')
    if status_filter:
        concerns = concerns.filter(status=status_filter)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        concerns = concerns.filter(category=category_filter)
    
    data = []
    for concern in concerns:
        data.append({
            'id': concern.id,
            'title': concern.title,
            'description': concern.description[:100] + '...' if len(concern.description) > 100 else concern.description,
            'category': concern.category,
            'category_display': concern.get_category_display(),
            'category_icon': concern.get_category_icon(),
            'status': concern.status,
            'status_display': concern.get_status_display(),
            'priority': concern.priority,
            'latitude': float(concern.latitude),
            'longitude': float(concern.longitude),
            'location': concern.location,
            'barangay': concern.barangay,
            'marker_color': concern.get_marker_color(),
            'created_at': concern.created_at.strftime('%B %d, %Y'),
        })
    
    return JsonResponse({'concerns': data})

def emergency_units_data(request):
    """API endpoint to get emergency units"""
    units = EmergencyUnit.objects.all()
    data = []
    for unit in units:
        data.append({
            'name': unit.name,
            'type': unit.unit_type,
            'type_display': unit.get_unit_type_display(),
            'lat': float(unit.latitude),
            'lng': float(unit.longitude),
            'contact': unit.contact_number
        })
    return JsonResponse({'units': data})

def concern_detail_view(request, pk):
    concern = get_object_or_404(Concern, pk=pk)
    
    # Only prevent viewing if archived AND user is not LGU
    if concern.is_archived and not request.user.is_lgu():
        messages.error(request, 'This concern has been archived.')
        return redirect('concerns:list')
    
    
    # Get comments
    comments = concern.comments.all()
    comment_form = CommentForm()

    # Calculate votes
    from django.db.models import Sum
    total_votes = concern.votes.aggregate(total=Sum('value'))['total'] or 0
    
    user_vote = 0
    if request.user.is_authenticated:
        vote_obj = concern.votes.filter(voter=request.user).first()
        if vote_obj:
            user_vote = vote_obj.value

    
    context = {
        'concern': concern,
        'comments': comments,
        'comment_form': comment_form,
        'can_edit': concern.can_be_edited() or (request.user.is_authenticated and request.user.is_lgu()),
        'is_locked': concern.is_locked,
        'is_lgu': request.user.is_authenticated and request.user.groups.filter(name='LGU').exists(),
        'is_status_pending': concern.status == 'PENDING',
        'is_status_in_progress': concern.status == 'IN_PROGRESS',
        'is_status_resolved': concern.status == 'RESOLVED',
        'is_status_closed': concern.status == 'CLOSED',
        'is_priority_low': concern.priority == 'LOW',
        'is_priority_medium': concern.priority == 'MEDIUM',
        'is_priority_high': concern.priority == 'HIGH',
        'is_priority_high': concern.priority == 'HIGH',
        'is_priority_urgent': concern.priority == 'URGENT',
        'total_votes': total_votes,
        'user_vote': user_vote,
    }
    return render(request, 'concerns/detail.html', context)


@login_required
def concern_add_comment_view(request, pk):
    """Add a comment to a concern"""
    concern = get_object_or_404(Concern, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.concern = concern
            comment.author = request.user
            comment.save()
            
            # Notify the concern reporter about the new comment
            notify_new_comment(concern, request.user)
            
            messages.success(request, 'Comment added successfully.')
            return redirect('concerns:detail', pk=pk)
    
    return redirect('concerns:detail', pk=pk)

def concern_create_view(request):
    if request.method == 'POST':
        form = ConcernForm(request.POST, request.FILES)
        if form.is_valid():
            concern = form.save(commit=False)
            
            # Handle Anonymous vs Logged-in and Inheritance of Location
            if request.user.is_authenticated:
                concern.reporter = request.user
                
                # Auto-fill geographic fields from user profile if not manually set/overridden
                # (Since these aren't in the form, they are blank on the object initially)
                if request.user.region:
                    concern.region = request.user.region
                if request.user.province:
                    concern.province = request.user.province
                
                # We could also infer missing municipal/barangay if blank, 
                # but the form requires them or user fills them.
            else:
                concern.reporter = None
                concern.is_anonymous = True
                if not concern.alias:
                    concern.alias = generate_random_alias()
            
            # AI Analysis
            try:
                from apps.ai_services.utils import analyze_concern
                messages.info(request, "AI is analyzing your report...")
                
                # Call Gemini
                analysis = analyze_concern(concern.title, concern.description)
                
                if analysis:
                    suggested_priority = analysis.get('priority', 'LOW')
                    concern.priority = suggested_priority
                    
                    suggested_category = analysis.get('category')
                    if concern.category == 'OTHER' and suggested_category:
                        concern.category = suggested_category
                    
                    ai_message = f"AI analyzed this report. Suggested Category: {suggested_category}, Priority: {suggested_priority}. {analysis.get('reasoning', '')}"
            except Exception as e:
                print(f"AI Error: {e}")
                ai_message = None

            concern.save()
            
            # Add AI reasoning as a comment
            if 'ai_message' in locals() and ai_message:
                from .models import Comment
                
                # Determine comment author (System/Admin if anon)
                if request.user.is_authenticated:
                    comment_author = request.user
                else:
                    User = get_user_model()
                    comment_author = User.objects.filter(is_superuser=True).first()
                
                if comment_author:
                    Comment.objects.create(
                        concern=concern,
                        author=comment_author, 
                        content=f"🤖 [System AI] {ai_message}"
                    )

            messages.success(request, 'Concern reported successfully!')
            return redirect('concerns:detail', pk=concern.pk)
    else:
        form = ConcernForm()
    
    return render(request, 'concerns/create.html', {'form': form})

@login_required
def concern_update_view(request, pk):
    concern = get_object_or_404(Concern, pk=pk)
    
    # Check permissions
    if not request.user.is_lgu() and concern.reporter != request.user:
        messages.error(request, 'You do not have permission to update this concern.')
        return redirect('concerns:list')
    
    # Check if archived
    if concern.is_archived:
        messages.error(request, 'Cannot update an archived concern.')
        return redirect('concerns:detail', pk=concern.pk)
    
    # Check if locked OR if status is not PENDING (for regular users)
    if not request.user.is_lgu():
        if concern.is_locked or concern.status != 'PENDING':
            messages.error(request, 'This concern can only be edited while it has PENDING status. It is currently being processed by LGU staff.')
            return redirect('concerns:detail', pk=concern.pk)
    
    if request.method == 'POST':
        form = ConcernUpdateForm(request.POST, request.FILES, instance=concern, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Concern updated successfully!')
            return redirect('concerns:detail', pk=concern.pk)
    else:
        form = ConcernUpdateForm(instance=concern, user=request.user)
    
    context = {
        'form': form,
        'concern': concern,
        'is_locked': concern.is_locked,
    }
    return render(request, 'concerns/update.html', context)

@login_required
def concern_delete_view(request, pk):
    concern = get_object_or_404(Concern, pk=pk)
    
    # Only LGU can archive concerns
    if not request.user.is_lgu():
        messages.error(request, 'Only LGU staff can archive concerns.')
        return redirect('concerns:detail', pk=concern.pk)
    
    # Check if already archived
    if concern.is_archived:
        messages.error(request, 'This concern is already archived.')
        return redirect('concerns:list')
    
    if request.method == 'POST':
        # Soft delete - move to archive instead of deleting
        concern.archive(request.user)
        messages.success(request, 'Concern has been moved to archive.')
        return redirect('concerns:list')
    
    return render(request, 'concerns/delete.html', {'concern': concern})

@login_required
def concern_archive_list_view(request):
    """View archived concerns - LGU only"""
    if not request.user.is_lgu():
        messages.error(request, 'Only LGU staff can view archived concerns.')
        return redirect('concerns:list')
    
    archived_concerns = Concern.objects.filter(is_archived=True)
    
    context = {
        'concerns': archived_concerns,
    }
    return render(request, 'concerns/archive.html', context)

@login_required
def concern_unarchive_view(request, pk):
    """Unarchive a concern - LGU only"""
    if not request.user.is_lgu():
        messages.error(request, 'Only LGU staff can unarchive concerns.')
        return redirect('concerns:list')
    
    concern = get_object_or_404(Concern, pk=pk)
    
    if request.method == 'POST':
        concern.unarchive()
        messages.success(request, 'Concern has been restored from archive.')
        return redirect('concerns:detail', pk=concern.pk)
    
    return render(request, 'concerns/unarchive.html', {'concern': concern})

@login_required
def concern_permanent_delete_view(request, pk):
    """Permanently delete a concern - LGU only"""
    if not request.user.is_lgu():
        messages.error(request, 'Only LGU staff can permanently delete concerns.')
        return redirect('concerns:list')
    
    concern = get_object_or_404(Concern, pk=pk)
    
    if not concern.is_archived:
        messages.error(request, 'Only archived concerns can be permanently deleted.')
        return redirect('concerns:detail', pk=concern.pk)
    
    if request.method == 'POST':
        concern_title = concern.title
        concern.delete()  # Actually delete from database
        messages.success(request, f'Concern "{concern_title}" has been permanently deleted.')
        return redirect('concerns:archive_list')
    
    return render(request, 'concerns/permanent_delete.html', {'concern': concern})

# Add this to apps/concerns/views.py

@login_required
def concern_update_status_view(request, pk):
    """Quick status update for LGU - handles the form from detail page"""
    if not request.user.is_lgu():
        messages.error(request, 'Only LGU staff can update concern status.')
        return redirect('concerns:detail', pk=pk)
    
    concern = get_object_or_404(Concern, pk=pk)
    
    if request.method == 'POST':
        # Check for quick actions
        quick_action = request.POST.get('quick_action')
        
        if quick_action == 'resolve':
            concern.status = 'RESOLVED'
            concern.resolved_at = timezone.now()
            concern.is_locked = True
            concern.save()
            messages.success(request, f'Concern "{concern.title}" marked as RESOLVED.')
        elif quick_action == 'close':
            concern.status = 'CLOSED'
            concern.resolved_at = timezone.now()
            concern.is_locked = True
            concern.save()
            messages.success(request, f'Concern "{concern.title}" has been CLOSED. It will no longer appear on the map or list.')
        else:
            # Regular status/priority update
            new_status = request.POST.get('status')
            new_priority = request.POST.get('priority')
            admin_notes = request.POST.get('admin_notes', '')
            
            # Check if status changed from PENDING to something else
            old_status = concern.status
            
            if new_status:
                concern.status = new_status
                
                # Auto-lock if moving from PENDING
                if old_status == 'PENDING' and new_status != 'PENDING':
                    concern.is_locked = True
                    messages.info(request, 'Concern has been locked. The reporter can no longer edit it.')
                
                # Set resolved_at if marked as resolved or closed
                if new_status in ['RESOLVED', 'CLOSED'] and not concern.resolved_at:
                    concern.resolved_at = timezone.now()
            
            if new_priority:
                concern.priority = new_priority
            
            concern.save()
            
            # You could save admin_notes to a separate model if you want to track them
            # For now, just show success message
            if admin_notes:
                messages.info(request, 'Admin notes recorded (feature to save notes can be added).')
            
            messages.success(request, 'Concern status and priority updated successfully!')
    
    return redirect('concerns:detail', pk=pk)


@login_required
def concern_vote_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)
        
    concern = get_object_or_404(Concern, pk=pk)
    
    # Prevent self-voting
    if concern.reporter == request.user:
        return JsonResponse({'error': 'You cannot vote on your own report.'}, status=403)
        
    vote_val = int(request.POST.get('value', 0))
    
    if vote_val not in [1, -1]:
        return JsonResponse({'error': 'Invalid vote value'}, status=400)
        
    vote, created = Vote.objects.get_or_create(
        voter=request.user,
        concern=concern,
        defaults={'value': vote_val}
    )
    
    # If vote exists, check if user is changing their vote or toggling off
    if not created:
        if vote.value == vote_val:
            # Toggle off (remove vote)
            vote.delete()
            # Revert points for reporter
            if concern.reporter:
                concern.reporter.points = models.F('points') - vote_val
                concern.reporter.save(update_fields=['points'])
            
            # Re-fetch for updated count
            concern.refresh_from_db()
            
            return JsonResponse({
                'status': 'removed',
                'points': concern.votes.aggregate(total=models.Sum('value'))['total'] or 0
            })
        else:
            # Change vote (e.g., +1 to -1)
            # Update reporter points: remove old value, add new value
            if concern.reporter:
                # e.g. was +1, now -1. Change is -2.
                # was -1, now +1. Change is +2.
                change = vote_val - vote.value
                concern.reporter.points = models.F('points') + change
                concern.reporter.save(update_fields=['points'])
                
            vote.value = vote_val
            vote.save()
            return JsonResponse({
                'status': 'changed',
                'points': concern.votes.aggregate(total=models.Sum('value'))['total'] or 0
            })
            
    # New vote
    if concern.reporter:
        concern.reporter.points = models.F('points') + vote_val
        concern.reporter.save(update_fields=['points'])
        
        # Notify the reporter about the vote
        notify_vote(concern, request.user, vote_val)
        
        # Karma Moderation Check (Refresh to get actual value)
        concern.reporter.refresh_from_db()
        current_points = concern.reporter.points
        
        # BAN THRESHOLD: -10
        if current_points <= -10 and concern.reporter.is_active:
            concern.reporter.is_active = False
            concern.reporter.save(update_fields=['is_active'])
            # We can't log them out directly here easily as it's an AJAX request initiated by another user
            # But they will be blocked on next request
            print(f"User {concern.reporter.username} blocked due to low karma ({current_points})")
            
        # WARNING THRESHOLD: -5
        elif current_points <= -5 and current_points > -10:
             # In a real app, send a notification. For now, we just acknowledge logic is hit.
             pass
        
    return JsonResponse({
        'status': 'voted',
        'points': concern.votes.aggregate(total=models.Sum('value'))['total'] or 0
    })

@login_required
def concern_flag_reporter_view(request, pk):
    if not request.user.is_lgu():
        messages.error(request, 'Only LGU staff can flag users.')
        return redirect('concerns:detail', pk=pk)
        
    concern = get_object_or_404(Concern, pk=pk)
    
    if not concern.reporter:
        messages.error(request, 'Cannot flag anonymous or missing reporter.')
        return redirect('concerns:detail', pk=pk)
        
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        concern.reporter.is_flagged_for_legal_action = True
        concern.reporter.legal_action_reason = reason
        concern.reporter.save()
        messages.success(request, f'User {concern.reporter.username} flagged for legal action.')
        
    return redirect('concerns:detail', pk=pk)


@login_required
def report_comment_view(request, comment_id):
    """Allow users to report inappropriate comments."""
    from .models import CommentReport
    
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Prevent self-reporting
    if comment.author == request.user:
        messages.error(request, "You cannot report your own comment.")
        return redirect('concerns:detail', pk=comment.concern.pk)
    
    # Check for duplicate reports
    existing_report = CommentReport.objects.filter(
        comment=comment, 
        reporter=request.user,
        status='PENDING'
    ).exists()
    
    if existing_report:
        messages.info(request, "You have already reported this comment.")
        return redirect('concerns:detail', pk=comment.concern.pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        if reason:
            CommentReport.objects.create(
                comment=comment,
                reporter=request.user,
                reason=reason
            )
            messages.success(request, "Comment reported. An admin will review it shortly.")
        else:
            messages.error(request, "Please provide a reason for your report.")
    
    return redirect('concerns:detail', pk=comment.concern.pk)
