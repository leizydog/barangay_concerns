import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("Creating migrations for accounts app...")
call_command('makemigrations', 'accounts')

print("\nCreating migrations for concerns app...")
call_command('makemigrations', 'concerns')

print("\nApplying all migrations...")
call_command('migrate')

print("\n" + "="*50)
print("Migrations created and applied successfully!")
print("="*50)
print("\nNow you can create a superuser.")
print("Run: python manage.py createsuperuser")