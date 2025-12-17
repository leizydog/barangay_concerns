import os
import django
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

print("=" * 60)
print("RENAMING APP: accounts → security_management")
print("=" * 60)

BASE_DIR = Path(__file__).resolve().parent

# Step 1: Check if old migrations exist
old_migrations = BASE_DIR / 'apps' / 'accounts' / 'migrations'
new_migrations = BASE_DIR / 'apps' / 'security_management' / 'migrations'

if old_migrations.exists() and not new_migrations.exists():
    print("\n✓ Copying migrations from accounts to security_management...")
    shutil.copytree(old_migrations, new_migrations)
    print("✓ Migrations copied successfully")
elif new_migrations.exists():
    print("\n✓ Migrations already exist in security_management")
else:
    print("\n✓ No existing migrations found")

# Step 2: Setup Django
django.setup()

from django.core.management import call_command
from django.db import connection

print("\n" + "=" * 60)
print("UPDATING DATABASE")
print("=" * 60)

# Step 3: Update django_migrations table
print("\nUpdating migration history...")
try:
    with connection.cursor() as cursor:
        # Check if accounts migrations exist
        cursor.execute("""
            SELECT COUNT(*) FROM django_migrations 
            WHERE app = 'accounts'
        """)
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Found {count} migration(s) for 'accounts' app")
            # Update app name in migrations table
            cursor.execute("""
                UPDATE django_migrations 
                SET app = 'security_management' 
                WHERE app = 'accounts'
            """)
            print("✓ Updated migration records")
        else:
            print("✓ No accounts migrations to update")
            
except Exception as e:
    print(f"✗ Error updating migrations: {e}")
    print("You may need to manually update the database")

# Step 4: Update content types
print("\nUpdating content types...")
try:
    from django.contrib.contenttypes.models import ContentType
    
    # Update User model content type
    user_ct = ContentType.objects.filter(app_label='accounts', model='user').first()
    if user_ct:
        user_ct.app_label = 'security_management'
        user_ct.save()
        print("✓ Updated User content type")
    else:
        print("✓ No accounts content types found")
        
except Exception as e:
    print(f"✗ Error updating content types: {e}")

# Step 5: Run migrations
print("\n" + "=" * 60)
print("APPLYING MIGRATIONS")
print("=" * 60)

try:
    print("\nCreating new migrations...")
    call_command('makemigrations', 'security_management')
    
    print("\nApplying migrations...")
    call_command('migrate')
    
    print("\n✓ All migrations applied successfully!")
    
except Exception as e:
    print(f"\n✗ Error with migrations: {e}")
    print("\nTry running these commands manually:")
    print("  python manage.py makemigrations security_management")
    print("  python manage.py migrate")

print("\n" + "=" * 60)
print("MIGRATION COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Run: python fix_templates.py")
print("2. Update config/settings.py")
print("3. Update config/urls.py") 
print("4. Update templates/organisms/navbar.html")
print("5. Update templates/pages/home.html")
print("6. Run: python manage.py runserver")
print("=" * 60)