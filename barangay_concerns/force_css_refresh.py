import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent

print("=" * 60)
print("FORCING STATIC FILES REFRESH")
print("=" * 60)

# Check if CSS file exists and show its size
css_file = BASE_DIR / 'static' / 'css' / 'style.css'
js_file = BASE_DIR / 'static' / 'js' / 'main.js'

print("\n1. Checking files...")
if css_file.exists():
    size = css_file.stat().st_size
    print(f"✓ CSS file found: {css_file}")
    print(f"  File size: {size:,} bytes")
    if size < 10000:
        print("  ⚠ WARNING: File seems too small! Make sure you copied ALL the CSS.")
else:
    print(f"✗ CSS file NOT found: {css_file}")

if js_file.exists():
    size = js_file.stat().st_size
    print(f"✓ JS file found: {js_file}")
    print(f"  File size: {size:,} bytes")
else:
    print(f"✗ JS file NOT found: {js_file}")

# Collect static files
print("\n2. Collecting static files...")
try:
    call_command('collectstatic', '--noinput', '--clear')
    print("✓ Static files collected")
except Exception as e:
    print(f"Note: {e}")
    print("This is okay - static files will still work in DEBUG mode")

print("\n" + "=" * 60)
print("CACHE CLEARING INSTRUCTIONS")
print("=" * 60)
print("""
Do ALL of these steps:

1. STOP the Django server (Ctrl+C)

2. CLEAR Django cache:
   - Delete the __pycache__ folders
   - Delete any .pyc files

3. HARD REFRESH your browser:
   - Chrome/Edge: Ctrl + Shift + R (or Ctrl + F5)
   - Firefox: Ctrl + Shift + R
   - Safari: Cmd + Shift + R
   
4. If that doesn't work, CLEAR BROWSER CACHE:
   - Chrome: Ctrl + Shift + Delete
   - Select "Cached images and files"
   - Click "Clear data"

5. RESTART Django server:
   python manage.py runserver

6. Open browser in INCOGNITO/PRIVATE mode:
   - This bypasses all caching
   - Chrome: Ctrl + Shift + N
   - Firefox: Ctrl + Shift + P

""")

print("=" * 60)
print("VERIFICATION STEPS")
print("=" * 60)
print("""
To verify the CSS is loading:

1. Open your browser's Developer Tools (F12)

2. Go to the "Network" tab

3. Refresh the page (Ctrl + F5)

4. Look for "style.css" in the list

5. Click on it and check:
   - Status should be "200"
   - Size should be around 20-30KB
   - Preview should show the new CSS code

If you see old CSS:
   - The browser is still caching
   - Try incognito mode
   - Or clear browser cache completely

""")

print("=" * 60)