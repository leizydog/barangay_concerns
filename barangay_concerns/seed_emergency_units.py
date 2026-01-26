
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.concerns.models import EmergencyUnit

# Clear existing
EmergencyUnit.objects.all().delete()

# Sample data centered around the user's focus (Manila area approx)
UNITS = [
    {
        'name': 'Barangay 123 Hall',
        'type': 'BARANGAY',
        'lat': 14.6091,
        'lng': 121.0223,
    },
    {
        'name': 'Manila Police District Station 8',
        'type': 'POLICE',
        'lat': 14.6150,
        'lng': 121.0300,
    },
    {
        'name': 'San Lazaro Fire Station',
        'type': 'FIRE',
        'lat': 14.6130,
        'lng': 120.9850,
    },
    {
        'name': 'UST Hospital',
        'type': 'HOSPITAL',
        'lat': 14.6110,
        'lng': 120.9890,
    },
     {
        'name': 'Barangay 456 Outpost',
        'type': 'BARANGAY',
        'lat': 14.6050,
        'lng': 121.0100,
    },
]

for unit in UNITS:
    u = EmergencyUnit.objects.create(
        name=unit['name'],
        unit_type=unit['type'],
        latitude=unit['lat'],
        longitude=unit['lng'],
        contact_number=f"09{random.randint(100000000, 999999999)}"
    )
    print(f"Created {u}")

print("Done seeding emergency units.")
