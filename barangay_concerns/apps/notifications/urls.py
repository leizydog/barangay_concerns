# apps/notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list_view, name='list'),
    path('<int:pk>/read/', views.notification_mark_read_view, name='mark_read'),
    path('mark-all-read/', views.notification_mark_all_read_view, name='mark_all_read'),
    path('<int:pk>/delete/', views.notification_delete_view, name='delete'),
    path('delete-all-read/', views.notification_delete_all_read_view, name='delete_all_read'),
    path('api/count/', views.notification_count_api, name='count_api'),
]
