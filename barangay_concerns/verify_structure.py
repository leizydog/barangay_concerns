import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

required_dirs = [
    'templates',
    'templates/atoms',
    'templates/molecules',
    'templates/organisms',
    'templates/auth',
    'templates/concerns',
    'templates/pages',
    'static',
    'static/css',
    'static/js',
]

required_files = [
    'templates/base.html',
    'templates/auth/login.html',
    'templates/auth/register.html',
    'templates/pages/home.html',
    'templates/concerns/list.html',
    'templates/concerns/detail.html',
    'templates/concerns/create.html',
    'templates/concerns/update.html',
    'templates/concerns/delete.html',
    'templates/concerns/map.html',  # Added this line
    'static/css/style.css',
    'static/js/main.js',
]

print("=" * 60)
print("PROJECT STRUCTURE VERIFICATION")
print("=" * 60)

print("\nChecking directories:")
missing_dirs = []
for dir_path in required_dirs:
    full_path = BASE_DIR / dir_path
    if full_path.exists():
        print(f"✓ {dir_path}")
    else:
        print(f"✗ {dir_path} - MISSING")
        missing_dirs.append(dir_path)

print("\nChecking required files:")
missing_files = []
for file_path in required_files:
    full_path = BASE_DIR / file_path
    if full_path.exists():
        print(f"✓ {file_path}")
    else:
        print(f"✗ {file_path} - MISSING")
        missing_files.append(file_path)

print("\n" + "=" * 60)
if missing_dirs or missing_files:
    print("ISSUES FOUND!")
    if missing_dirs:
        print(f"\nMissing {len(missing_dirs)} directories")
    if missing_files:
        print(f"Missing {len(missing_files)} files")
    print("\nCreating missing directories...")
    for dir_path in missing_dirs:
        full_path = BASE_DIR / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {dir_path}")
else:
    print("ALL STRUCTURE OK!")
print("=" * 60)
