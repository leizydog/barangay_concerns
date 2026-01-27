# apps/concerns/urls.py
from django.urls import path
from . import views

app_name = 'concerns'

urlpatterns = [
    path('', views.concern_list_view, name='list'),
    path('map/', views.concern_map_view, name='map'),
    path('api/map-data/', views.concern_map_data, name='map_data'),
    path('api/emergency-units/', views.emergency_units_data, name='emergency_units_data'),
    path('archive/', views.concern_archive_list_view, name='archive_list'),
    path('<int:pk>/', views.concern_detail_view, name='detail'),
    path('<int:pk>/update/', views.concern_update_view, name='update'),
    path('<int:pk>/update-status/', views.concern_update_status_view, name='update_status'),
    path('<int:pk>/delete/', views.concern_delete_view, name='delete'),
    path('<int:pk>/comment/', views.concern_add_comment_view, name='add_comment'),
    path('<int:pk>/unarchive/', views.concern_unarchive_view, name='unarchive'),
    path('<int:pk>/permanent-delete/', views.concern_permanent_delete_view, name='permanent_delete'),
    path('<int:pk>/vote/', views.concern_vote_view, name='vote'),
    path('<int:pk>/flag/', views.concern_flag_reporter_view, name='flag_reporter'),
    path('create/', views.concern_create_view, name='create'),
]