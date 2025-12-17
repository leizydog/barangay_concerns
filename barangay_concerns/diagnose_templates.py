import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

BASE_DIR = Path(__file__).resolve().parent

print("=" * 60)
print("TEMPLATE CONFIGURATION DIAGNOSTICS")
print("=" * 60)

# Check settings
print("\n1. TEMPLATE SETTINGS:")
print(f"   APP_DIRS: {settings.TEMPLATES[0]['APP_DIRS']}")
print(f"   DIRS: {settings.TEMPLATES[0]['DIRS']}")

# Check installed apps
print("\n2. INSTALLED APPS:")
for app in settings.INSTALLED_APPS:
    if 'security' in app or 'concerns' in app:
        print(f"   ✓ {app}")

# Check if security_management app exists
print("\n3. APP DIRECTORY CHECK:")
security_mgmt = BASE_DIR / 'apps' / 'security_management'
if security_mgmt.exists():
    print(f"   ✓ security_management app exists")
    
    # Check for templates
    app_templates = security_mgmt / 'templates' / 'security_management'
    if app_templates.exists():
        print(f"   ✓ App templates directory exists")
        print(f"     Path: {app_templates}")
        
        # List template files
        print("\n4. TEMPLATE FILES IN APP:")
        for template_file in app_templates.rglob('*.html'):
            relative = template_file.relative_to(app_templates)
            print(f"     ✓ security_management/{relative}")
    else:
        print(f"   ✗ App templates directory NOT found")
        print(f"     Expected: {app_templates}")
else:
    print(f"   ✗ security_management app NOT found")

# Check root templates
print("\n5. ROOT TEMPLATES DIRECTORY:")
root_templates = BASE_DIR / 'templates'
if root_templates.exists():
    print(f"   ✓ Root templates directory exists")
    if (root_templates / 'security_management').exists():
        print(f"   ✓ security_management templates in root")
        for template_file in (root_templates / 'security_management').rglob('*.html'):
            relative = template_file.relative_to(root_templates)
            print(f"     ✓ {relative}")
    else:
        print(f"   ✗ No security_management folder in root templates")
else:
    print(f"   ✗ Root templates directory NOT found")

# Try to load templates
print("\n6. TEMPLATE LOADING TEST:")
templates_to_test = [
    'security_management/pages/login.html',
    'security_management/pages/register.html',
    'security_management/organisms/auth_card.html',
    'base.html',
]

for template_name in templates_to_test:
    try:
        template = get_template(template_name)
        print(f"   ✓ {template_name} - FOUND")
        print(f"     Location: {template.origin.name}")
    except TemplateDoesNotExist as e:
        print(f"   ✗ {template_name} - NOT FOUND")
        print(f"     Error: {e}")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
print("=" * 60)

# Recommendations
print("\nRECOMMENDATIONS:")
app_templates_exist = (BASE_DIR / 'apps' / 'security_management' / 'templates' / 'security_management').exists()
root_templates_exist = (BASE_DIR / 'templates' / 'security_management').exists()

if app_templates_exist and not root_templates_exist:
    print("✓ Templates are in app directory (correct for APP_DIRS=True)")
    print("  If templates not loading, check:")
    print("  1. apps.py - ensure name='apps.security_management'")
    print("  2. settings.py - ensure 'apps.security_management' in INSTALLED_APPS")
    print("  3. Restart Django server after changes")
elif not app_templates_exist and root_templates_exist:
    print("✓ Templates are in root directory (correct for DIRS setting)")
elif app_templates_exist and root_templates_exist:
    print("⚠ Templates exist in BOTH locations")
    print("  Django will use root templates first (DIRS takes precedence)")
else:
    print("✗ No templates found in either location!")
    print("  Run: python fix_templates.py")

print("=" * 60)