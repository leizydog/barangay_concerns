from django.contrib import admin
from .models import Concern

@admin.register(Concern)
class ConcernAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'priority', 'reporter', 'created_at']
    list_filter = ['status', 'category', 'priority', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'created_at'