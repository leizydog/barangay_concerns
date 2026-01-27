import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.concerns.models import EmergencyUnit

# Overpass API URL
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Bounding box for Plaridel, Bulacan and surroundings (approx)
# south,west,north,east
BBOX = "14.80,120.80,15.00,121.00"

QUERY = f"""
[out:json];
(
  node["amenity"="police"]({BBOX});
  way["amenity"="police"]({BBOX});
  relation["amenity"="police"]({BBOX});
  
  node["amenity"="fire_station"]({BBOX});
  way["amenity"="fire_station"]({BBOX});
  relation["amenity"="fire_station"]({BBOX});
  
  node["amenity"="hospital"]({BBOX});
  way["amenity"="hospital"]({BBOX});
  relation["amenity"="hospital"]({BBOX});
  
  node["amenity"="clinic"]({BBOX});
  way["amenity"="clinic"]({BBOX});
  
  node["name"~"Barangay",i]({BBOX});
  way["name"~"Barangay",i]({BBOX});
);
out center;
"""

def fetch_data():
    print("Fetching data from OpenStreetMap...")
    try:
        response = requests.get(OVERPASS_URL, params={'data': QUERY})
        response.raise_for_status()
        data = response.json()
        return data.get('elements', [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def save_units(elements):
    count = 0
    # Optional: Clear existing data? 
    # emergency_units = EmergencyUnit.objects.all().delete()
    # print("Cleared existing units.")
    
    # Let's clean up old seed data if it looks fake "Barangay 123 Hall"
    EmergencyUnit.objects.filter(name__contains="Barangay 123").delete()

    existing_names = set(EmergencyUnit.objects.values_list('name', flat=True))

    for el in elements:
        tags = el.get('tags', {})
        name = tags.get('name', tags.get('amenity', 'Unknown'))
        
        if not name or name in existing_names:
            continue
            
        # Determine type
        amenity = tags.get('amenity', '')
        u_type = 'BARANGAY' # Default fallback if name has Barangay
        
        if amenity == 'police':
            u_type = 'POLICE'
        elif amenity == 'fire_station':
            u_type = 'FIRE'
        elif amenity in ['hospital', 'clinic', 'doctors']:
            u_type = 'HOSPITAL'
        elif 'Barangay' in name:
            u_type = 'BARANGAY'
        else:
            # Skip unconnected stuff matched by broad queries if any
            if 'Barangay' not in name:
                continue

        lat = el.get('lat')
        lon = el.get('lon')
        
        # For ways/relations, use 'center'
        if not lat and 'center' in el:
            lat = el['center']['lat']
            lon = el['center']['lon']
            
        if lat and lon:
            EmergencyUnit.objects.create(
                name=name,
                unit_type=u_type,
                latitude=lat,
                longitude=lon,
                contact_number=tags.get('phone', tags.get('contact:phone', ''))
            )
            existing_names.add(name)
            count += 1
            
    print(f"Imported {count} new emergency units/outposts.")

if __name__ == "__main__":
    elements = fetch_data()
    if elements:
        save_units(elements)
    else:
        print("No data found.")
