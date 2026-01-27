import os
import django
from django.db.models import Count, Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.concerns.models import EmergencyUnit

print("--- Emergency Unit Summary ---")
counts = EmergencyUnit.objects.values('unit_type').annotate(total=Count('id'))
for c in counts:
    print(f"{c['unit_type']}: {c['total']}")

print("\n--- Contact Numbers ---")
with_contact = EmergencyUnit.objects.exclude(contact_number='').count()
print(f"Total with contact number: {with_contact}")

print("\n--- Sample Barangay Halls ---")
barangays = EmergencyUnit.objects.filter(unit_type='BARANGAY')[:5]
for b in barangays:
    print(f"{b.name} - {b.contact_number}")

print("\n--- Sample Police Stations ---")
police = EmergencyUnit.objects.filter(unit_type='POLICE')[:5]
for p in police:
    print(f"{p.name} - {p.contact_number}")
