import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.security_management.models import User

print("=" * 60)
print("UPDATE ADMIN ROLE")
print("=" * 60)

# Get the superuser (usually the first user created)
try:
    superusers = User.objects.filter(is_superuser=True)
    
    if superusers.exists():
        for user in superusers:
            user.role = 'LGU'
            user.save()
            print(f"\n✓ Updated user '{user.username}' to LGU role")
    else:
        print("\n✗ No superuser found. Please create one first.")
        print("   Run: python manage.py createsuperuser")
except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n" + "=" * 60)
print("You can now login as LGU staff!")
print("=" * 60)