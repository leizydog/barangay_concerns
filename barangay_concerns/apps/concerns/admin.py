from django.contrib import admin
from .models import Concern

@admin.register(Concern)
class ConcernAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'priority', 'region', 'province', 'reporter', 'created_at', 'is_archived']
    list_filter = ['status', 'category', 'priority', 'region', 'province', 'is_archived', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'created_at'