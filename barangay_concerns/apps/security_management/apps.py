from django.apps import AppConfig

# 1. Class name changed from AccountsConfig
class SecurityManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # 2. App name/path changed from 'apps.accounts'
    name = 'apps.security_management'

# Note: Any line like 'from . import views' has been removed to prevent the AppRegistryNotReady error.