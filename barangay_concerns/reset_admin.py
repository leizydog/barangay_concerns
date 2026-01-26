
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    u, created = User.objects.get_or_create(username='admin')
    if created:
        u.email = 'admin@example.com'
    u.set_password('admin123')
    u.is_staff = True
    u.is_superuser = True
    u.role = 'LGU' # Ensure they can see LGU features
    u.save()
    print("User 'admin' with password 'admin123' is ready.")
except Exception as e:
    print(f"Error: {e}")
