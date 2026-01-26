# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('accounts/', include('apps.security_management.urls')),  # Changed but keep /accounts/ URL prefix
    path('concerns/', include('apps.concerns.urls')),
    path('notifications/', include('apps.notifications.urls')),  # Notification system
    path('analytics/', include('apps.analytics.urls')),          # Data & Analytics
    path('ai/', include('apps.ai_services.urls')),               # AI Chatbot & Services
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)