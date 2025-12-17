# apps/concerns/management/commands/seed_concerns.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.concerns.models import Concern
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample concerns in Bulacan area'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create users first
        self.create_users()
        
        # Create concerns
        self.create_concerns()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))

    def create_users(self):
        """Create sample users if they don't exist"""
        # Create LGU staff
        if not User.objects.filter(username='lgu_admin').exists():
            User.objects.create_user(
                username='lgu_admin',
                email='lgu@bulacan.gov.ph',
                password='admin123',
                role='LGU',
                first_name='Juan',
                last_name='Dela Cruz',
                phone_number='09171234567',
                municipality='Malolos',
                barangay='Barasoain'
            )
            self.stdout.write(self.style.SUCCESS('Created LGU admin user'))

        # Create regular users
        regular_users = [
            {
                'username': 'maria_santos',
                'email': 'maria@example.com',
                'first_name': 'Maria',
                'last_name': 'Santos',
                'phone_number': '09181234567',
                'municipality': 'Malolos',
                'barangay': 'Barasoain'
            },
            {
                'username': 'pedro_reyes',
                'email': 'pedro@example.com',
                'first_name': 'Pedro',
                'last_name': 'Reyes',
                'phone_number': '09191234567',
                'municipality': 'San Jose del Monte',
                'barangay': 'Ciudad Real'
            },
            {
                'username': 'ana_garcia',
                'email': 'ana@example.com',
                'first_name': 'Ana',
                'last_name': 'Garcia',
                'phone_number': '09201234567',
                'municipality': 'Meycauayan',
                'barangay': 'Calvario'
            },
            {
                'username': 'jose_mendoza',
                'email': 'jose@example.com',
                'first_name': 'Jose',
                'last_name': 'Mendoza',
                'phone_number': '09211234567',
                'municipality': 'Marilao',
                'barangay': 'Poblacion'
            },
        ]

        for user_data in regular_users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    password='user123',
                    role='USER',
                    **user_data
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {user_data["username"]}'))

    def create_concerns(self):
        """Create sample concerns in Bulacan locations"""
        
        # Get users
        lgu_user = User.objects.get(username='lgu_admin')
        regular_users = User.objects.filter(role='USER')

        # Bulacan locations with coordinates (lat, lng)
        locations = [
            {
                'location': 'Barasoain Church, Malolos',
                'barangay': 'Barasoain',
                'municipality': 'Malolos',
                'latitude': Decimal('14.8453'),
                'longitude': Decimal('120.8114')
            },
            {
                'location': 'MacArthur Highway, San Jose del Monte',
                'barangay': 'Ciudad Real',
                'municipality': 'San Jose del Monte',
                'latitude': Decimal('14.8138'),
                'longitude': Decimal('121.0452')
            },
            {
                'location': 'Meycauayan Public Market',
                'barangay': 'Calvario',
                'municipality': 'Meycauayan',
                'latitude': Decimal('14.7353'),
                'longitude': Decimal('120.9553')
            },
            {
                'location': 'Marilao-Meycauayan Road',
                'barangay': 'Poblacion',
                'municipality': 'Marilao',
                'latitude': Decimal('14.7581'),
                'longitude': Decimal('120.9472')
            },
            {
                'location': 'Plaridel Town Plaza',
                'barangay': 'Poblacion',
                'municipality': 'Plaridel',
                'latitude': Decimal('14.8853'),
                'longitude': Decimal('120.8572')
            },
            {
                'location': 'Baliuag Public Market',
                'barangay': 'Poblacion',
                'municipality': 'Baliuag',
                'latitude': Decimal('14.9544'),
                'longitude': Decimal('120.8964')
            },
            {
                'location': 'Santa Maria Municipal Hall',
                'barangay': 'Poblacion',
                'municipality': 'Santa Maria',
                'latitude': Decimal('14.8197'),
                'longitude': Decimal('120.9569')
            },
            {
                'location': 'Norzagaray Bridge',
                'barangay': 'Poblacion',
                'municipality': 'Norzagaray',
                'latitude': Decimal('14.9136'),
                'longitude': Decimal('121.0544')
            },
            {
                'location': 'Bocaue River Road',
                'barangay': 'Bunlo',
                'municipality': 'Bocaue',
                'latitude': Decimal('14.7997'),
                'longitude': Decimal('120.9244')
            },
            {
                'location': 'Balagtas Town Center',
                'barangay': 'Poblacion',
                'municipality': 'Balagtas',
                'latitude': Decimal('14.8156'),
                'longitude': Decimal('120.8686')
            },
        ]

        # Sample concerns data
        concerns_data = [
            {
                'title': 'Severe Flooding on Main Road',
                'description': 'Heavy flooding occurs every time it rains heavily. The drainage system appears to be clogged or insufficient. Water reaches knee-deep levels, making the road impassable for vehicles and dangerous for pedestrians.',
                'category': 'FLOOD',
                'status': 'PENDING',
                'priority': 'HIGH'
            },
            {
                'title': 'Large Potholes Causing Accidents',
                'description': 'Multiple large potholes have developed on this road section. Several motorcycle accidents have already occurred. The potholes are particularly dangerous at night when visibility is poor.',
                'category': 'ROAD',
                'status': 'IN_PROGRESS',
                'priority': 'URGENT'
            },
            {
                'title': 'Uncollected Garbage for 2 Weeks',
                'description': 'Garbage collection has not been conducted for the past two weeks. Waste is piling up and creating health hazards. Foul odor is affecting nearby residents and attracting pests.',
                'category': 'WASTE',
                'status': 'PENDING',
                'priority': 'HIGH'
            },
            {
                'title': 'Frequent Power Interruptions',
                'description': 'The area experiences daily power outages lasting 2-4 hours. This is affecting businesses and causing food spoilage in households. The issue has been ongoing for the past month.',
                'category': 'ELECTRICITY',
                'status': 'IN_PROGRESS',
                'priority': 'MEDIUM'
            },
            {
                'title': 'No Water Supply for 3 Days',
                'description': 'Water supply has been cut off for three consecutive days without prior notice. Residents are struggling to access clean water for drinking and daily needs.',
                'category': 'WATER',
                'status': 'RESOLVED',
                'priority': 'URGENT'
            },
            {
                'title': 'Broken Streetlights Compromising Safety',
                'description': 'Most streetlights in the area are not functioning, creating a safety concern especially at night. There have been reports of increased criminal activity in the poorly lit areas.',
                'category': 'SAFETY',
                'status': 'PENDING',
                'priority': 'HIGH'
            },
            {
                'title': 'Damaged Bridge Railing',
                'description': 'The bridge railing has been damaged in several sections, posing a serious safety risk for motorists and pedestrians. Immediate repair is needed to prevent accidents.',
                'category': 'ROAD',
                'status': 'IN_PROGRESS',
                'priority': 'URGENT'
            },
            {
                'title': 'Illegal Dumping Site',
                'description': 'An illegal dumping site has formed near the residential area. Various types of waste including construction debris and household garbage are being dumped indiscriminately.',
                'category': 'WASTE',
                'status': 'PENDING',
                'priority': 'MEDIUM'
            },
            {
                'title': 'Stray Dogs Roaming the Streets',
                'description': 'A pack of stray dogs has been roaming the neighborhood, causing safety concerns especially for children and elderly residents. Some residents have been chased and scared.',
                'category': 'SAFETY',
                'status': 'PENDING',
                'priority': 'MEDIUM'
            },
            {
                'title': 'Cracked Road Pavement',
                'description': 'Large cracks have appeared on the main road pavement. The cracks are widening and could lead to more serious road damage if not addressed soon.',
                'category': 'ROAD',
                'status': 'RESOLVED',
                'priority': 'LOW'
            },
            {
                'title': 'Water Pipe Leak',
                'description': 'A major water pipe leak has been observed, causing water wastage and creating muddy conditions on the road. The leak needs immediate attention.',
                'category': 'WATER',
                'status': 'IN_PROGRESS',
                'priority': 'HIGH'
            },
            {
                'title': 'Overflowing Canal During Rain',
                'description': 'The drainage canal overflows during moderate to heavy rain, flooding nearby houses and making streets impassable. Regular maintenance and dredging are needed.',
                'category': 'FLOOD',
                'status': 'PENDING',
                'priority': 'HIGH'
            },
            {
                'title': 'Exposed Electrical Wires',
                'description': 'Electrical wires are hanging loosely and some are exposed, creating a serious electrocution hazard. This is extremely dangerous especially during rainy weather.',
                'category': 'ELECTRICITY',
                'status': 'PENDING',
                'priority': 'URGENT'
            },
            {
                'title': 'Narrow Road Needs Widening',
                'description': 'The road is too narrow for two-way traffic, causing frequent traffic congestion and near-miss accidents. Road widening project is urgently needed.',
                'category': 'ROAD',
                'status': 'PENDING',
                'priority': 'LOW'
            },
            {
                'title': 'Poor Drainage System',
                'description': 'The existing drainage system is inadequate and poorly maintained. Standing water remains on streets for days after rain, creating breeding grounds for mosquitoes.',
                'category': 'FLOOD',
                'status': 'RESOLVED',
                'priority': 'MEDIUM'
            },
        ]

        # Create concerns
        created_count = 0
        for i, concern_data in enumerate(concerns_data):
            location = locations[i % len(locations)]
            reporter = random.choice(regular_users)
            
            # Check if concern already exists
            if not Concern.objects.filter(
                title=concern_data['title'],
                location=location['location']
            ).exists():
                concern = Concern.objects.create(
                    title=concern_data['title'],
                    description=concern_data['description'],
                    category=concern_data['category'],
                    location=location['location'],
                    barangay=location['barangay'],
                    municipality=location['municipality'],
                    latitude=location['latitude'],
                    longitude=location['longitude'],
                    status=concern_data['status'],
                    priority=concern_data['priority'],
                    reporter=reporter,
                )
                
                # For IN_PROGRESS and RESOLVED concerns, lock them
                if concern.status in ['IN_PROGRESS', 'RESOLVED']:
                    concern.is_locked = True
                    concern.save()
                
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created concern: {concern.title}'))

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} concerns in total'))