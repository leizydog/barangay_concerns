import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.concerns.models import EmergencyUnit

def generate_phone(unit_type):
    if unit_type == 'POLICE':
        return f"044-79{random.randint(0, 9)}-{random.randint(1000, 9999)}"
    elif unit_type == 'FIRE':
        return f"044-76{random.randint(0, 9)}-{random.randint(1000, 9999)}"
    else:
        # Mobile for Barangays usually
        return f"09{random.choice(['17', '18', '27', '66', '08'])}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

units = EmergencyUnit.objects.filter(contact_number='')
print(f"Backfilling {units.count()} units with no contact number...")

for u in units:
    u.contact_number = generate_phone(u.unit_type)
    u.save()

print("Done.")
