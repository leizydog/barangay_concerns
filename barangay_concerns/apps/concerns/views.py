# apps/concerns/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Concern
from .forms import ConcernForm, ConcernUpdateForm
from django.utils import timezone

@login_required
def concern_list_view(request):
    # Exclude archived and closed concerns - show ALL to everyone
    concerns = Concern.objects.filter(is_archived=False).exclude(status='CLOSED')
    
    # NO FILTERING BY USER - everyone can see all reports
    
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
    }
    return render(request, 'concerns/list.html', context)

@login_required
def concern_map_view(request):
    """Display all concerns on an interactive map - exclude closed and archived"""
    concerns = Concern.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False,
        is_archived=False
    ).exclude(status='CLOSED')
    
    # NO FILTERING BY USER - everyone can see all reports on map
    
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

@login_required
def concern_map_data(request):
    """API endpoint to get concern data as JSON for map markers - exclude closed and archived"""
    concerns = Concern.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False,
        is_archived=False
    ).exclude(status='CLOSED')
    
    # NO FILTERING BY USER - everyone can see all reports
    
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

@login_required
def concern_detail_view(request, pk):
    concern = get_object_or_404(Concern, pk=pk)
    
    # Remove the permission check - everyone can view all concerns
    # Only prevent viewing if archived AND user is not LGU
    if concern.is_archived and not request.user.is_lgu():
        messages.error(request, 'This concern has been archived.')
        return redirect('concerns:list')
    
    context = {
        'concern': concern,
        'can_edit': concern.can_be_edited() or request.user.is_lgu(),
        'is_locked': concern.is_locked,
    }
    return render(request, 'concerns/detail.html', context)

@login_required
def concern_create_view(request):
    if request.method == 'POST':
        form = ConcernForm(request.POST, request.FILES)
        if form.is_valid():
            concern = form.save(commit=False)
            concern.reporter = request.user
            concern.save()
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


