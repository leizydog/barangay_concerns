from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, F
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
import csv
from apps.concerns.models import Concern

def is_lgu(user):
    return user.is_authenticated and user.is_lgu()

@login_required
@user_passes_test(is_lgu)
def dashboard_view(request):
    """
    Main analytics dashboard for LGU staff.
    """
    # 1. Overview Cards
    total_concerns = Concern.objects.count()
    pending_count = Concern.objects.filter(status='PENDING').count()
    resolved_count = Concern.objects.filter(status='RESOLVED').count()
    in_progress_count = Concern.objects.filter(status='IN_PROGRESS').count()
    archived_count = Concern.objects.filter(is_archived=True).count()
    
    # Resolution Rate
    resolution_rate = 0
    if total_concerns > 0:
        resolution_rate = (resolved_count / total_concerns) * 100
        
    # 2. Concerns by Category (Bar Chart)
    concerns_by_category = Concern.objects.values('category').annotate(count=Count('id')).order_by('-count')
    category_labels = [dict(Concern.CATEGORY_CHOICES).get(item['category'], item['category']) for item in concerns_by_category]
    category_data = [item['count'] for item in concerns_by_category]
    
    # 3. Concerns by Status (Pie Chart)
    concerns_by_status = Concern.objects.values('status').annotate(count=Count('id'))
    status_labels = [dict(Concern.STATUS_CHOICES).get(item['status'], item['status']) for item in concerns_by_status]
    status_data = [item['count'] for item in concerns_by_status]
    
    # 4. Recent Trends (Last 30 days) (Line Chart)
    last_30_days = timezone.now() - timedelta(days=30)
    daily_trends = Concern.objects.filter(created_at__gte=last_30_days)\
        .annotate(date=TruncDay('created_at'))\
        .values('date')\
        .annotate(count=Count('id'))\
        .order_by('date')
        
    trend_labels = [item['date'].strftime('%Y-%m-%d') for item in daily_trends]
    trend_data = [item['count'] for item in daily_trends]
    
    context = {
        'total_concerns': total_concerns,
        'pending_count': pending_count,
        'resolved_count': resolved_count,
        'in_progress_count': in_progress_count,
        'archived_count': archived_count,
        'resolution_rate': round(resolution_rate, 1),
        
        # Chart Data
        'category_labels': category_labels,
        'category_data': category_data,
        'status_labels': status_labels,
        'status_data': status_data,
        'trend_labels': trend_labels,
        'trend_data': trend_data,
    }
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
@user_passes_test(is_lgu)
def export_data_view(request):
    """
    Export concern data to CSV.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="concerns_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Category', 'Status', 'Priority', 'Reporter', 'Location', 'Created At', 'Resolved At'])
    
    concerns = Concern.objects.all().order_by('-created_at')
    
    for concern in concerns:
        writer.writerow([
            concern.pk,
            concern.title,
            concern.get_category_display(),
            concern.get_status_display(),
            concern.get_priority_display(),
            'Anonymous' if concern.is_anonymous else (concern.reporter.get_full_name() if concern.reporter else 'Unknown'),
            f"{concern.barangay}, {concern.municipality}",
            concern.created_at.strftime('%Y-%m-%d %H:%M'),
            concern.resolved_at.strftime('%Y-%m-%d %H:%M') if concern.resolved_at else ''
        ])
        
    return response
