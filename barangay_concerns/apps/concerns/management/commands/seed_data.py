from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.concerns.models import Concern, Comment
from apps.notifications.models import Notification
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # 1. Create Users
        users = []
        user_data = [
            ('juan_cruz', 'Juan', 'Cruz', 'RESIDENT'),
            ('maria_santos', 'Maria', 'Santos', 'RESIDENT'),
            ('pedro_reyes', 'Pedro', 'Reyes', 'LGU'),
            ('anna_lim', 'Anna', 'Lim', 'LGU'),
        ]
        
        for username, first, last, role in user_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': first,
                    'last_name': last,
                    'role': role,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)
            
        # Get LGU user for assignment
        lgu_user = User.objects.filter(role='LGU').first()
        
        # 2. Create Concerns
        categories = ['FLOOD', 'ROAD', 'WASTE', 'ELECTRICITY', 'WATER', 'SAFETY', 'HEALTH']
        statuses = ['PENDING', 'IN_PROGRESS', 'RESOLVED', 'CLOSED']
        priorities = ['LOW', 'MEDIUM', 'HIGH', 'URGENT']
        
        descriptions = [
            "Heavy flooding in our street after the rain.",
            "Big pothole causing traffic.",
            "Garbage truck hasn't arrived for 3 days.",
            "Street light is flickering and dark at night.",
            "Low water pressure in the morning.",
            "Suspicious person loitering near the park.",
            "Mosquito breeding ground in stagnant water."
        ]
        
        # Create 30 concerns with varying dates for analytics
        for i in range(30):
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            created_at = timezone.now() - timedelta(days=days_ago)
            
            category = random.choice(categories)
            status = random.choice(statuses)
            
            # If resolved, set resolved_at
            resolved_at = None
            if status in ['RESOLVED', 'CLOSED']:
                resolved_days = days_ago - random.randint(0, days_ago)
                resolved_at = timezone.now() - timedelta(days=resolved_days)
            
            reporter = random.choice([u for u in users if u.role == 'RESIDENT'])
            
            concern = Concern.objects.create(
                title=f"{category.title()} Issue #{i+1}",
                description=random.choice(descriptions),
                category=category,
                priority=random.choice(priorities),
                status=status,
                reporter=reporter,
                barangay="San Isidro",
                municipality="Makati",
                location="Main St.",
                latitude=14.5 + (random.random() * 0.1),
                longitude=121.0 + (random.random() * 0.1),
                created_at=created_at
            )
            
            # Hack to set created_at (auto_now_add usually prevents manual set)
            Concern.objects.filter(pk=concern.pk).update(created_at=created_at)
            if resolved_at:
                Concern.objects.filter(pk=concern.pk).update(resolved_at=resolved_at)
                
            self.stdout.write(f'Created concern: {concern.title}')
            
            # Add comments
            if random.random() > 0.5:
                Comment.objects.create(
                    concern=concern,
                    author=lgu_user,
                    content="We have received your report and are validating it."
                )
        
        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))
