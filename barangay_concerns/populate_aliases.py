
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.concerns.utils import generate_random_alias

User = get_user_model()

users = User.objects.filter(alias__isnull=True)  # Or blank
for user in users:
    if not user.alias:
        new_alias = generate_random_alias()
        # Ensure unique
        while User.objects.filter(alias=new_alias).exists():
            new_alias = generate_random_alias()
        
        user.alias = new_alias
        user.save()
        print(f"Assigned alias '{new_alias}' to user '{user.username}'")

print("Done.")
