from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Read the content from the artifacts above and save to files
print("=" * 60)
print("UPDATING TEMPLATES WITH MAP FEATURES")
print("=" * 60)

print("\nPlease manually copy the following files from the artifacts above:")
print("\n1. Updated Concern Model (apps/concerns/models.py)")
print("2. Updated Concern Forms (apps/concerns/forms.py)")
print("3. Updated Concern Views (apps/concerns/views.py)")
print("4. Updated Concern URLs (apps/concerns/urls.py)")
print("5. Updated Navbar (templates/organisms/navbar.html)")
print("6. Map View Template (templates/concerns/map.html)")
print("7. Updated Create Template (templates/concerns/create.html)")
print("8. Updated Detail Template (templates/concerns/detail.html)")

print("\n" + "=" * 60)
print("INSTRUCTIONS")
print("=" * 60)
print("\nFollow these steps:")
print("\n1. Copy all the updated code from the artifacts")
print("2. Replace the content in the respective files")
print("3. Run: python update_model.py")
print("4. Run: python manage.py runserver")
print("\n" + "=" * 60)