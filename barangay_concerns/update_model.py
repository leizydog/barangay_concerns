import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command

print("=" * 60)
print("UPDATING DATABASE WITH MAP FIELDS")
print("=" * 60)

print("\n1. Creating migrations for map fields...")
try:
    call_command('makemigrations', 'concerns')
    print("✓ Migrations created successfully")
except Exception as e:
    print(f"✗ Error creating migrations: {e}")

print("\n2. Applying migrations...")
try:
    call_command('migrate')
    print("✓ Migrations applied successfully")
except Exception as e:
    print(f"✗ Error applying migrations: {e}")

print("\n" + "=" * 60)
print("DATABASE UPDATE COMPLETE!")
print("=" * 60)
print("\nNew fields added:")
print("- latitude (Decimal)")
print("- longitude (Decimal)")
print("\nYou can now use the map feature when reporting concerns!")
print("=" * 60)