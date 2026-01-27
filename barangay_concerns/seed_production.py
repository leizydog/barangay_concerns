"""
Seed script for production database.
Run with: python manage.py shell < seed_production.py
"""
import os
import sys
import django
import random
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.concerns.models import Concern, Comment, CommentReport, Vote
from apps.security_management.models import Announcement

User = get_user_model()

# ========== CONFIGURATION ==========
NUM_USERS = 15
NUM_CONCERNS = 25
COMMENTS_PER_CONCERN = (1, 5)  # Random range

# Philippine locations for realistic data
REGIONS = ['NCR', 'Region III', 'Region IV-A', 'Region VII']
PROVINCES = {
    'NCR': ['Metro Manila'],
    'Region III': ['Bulacan', 'Pampanga', 'Tarlac'],
    'Region IV-A': ['Cavite', 'Laguna', 'Batangas', 'Rizal'],
    'Region VII': ['Cebu', 'Bohol'],
}
MUNICIPALITIES = ['Quezon City', 'Manila', 'Makati', 'Pasig', 'Caloocan', 'Taguig', 'Parañaque', 'Marikina', 'Las Piñas', 'Muntinlupa']
BARANGAYS = ['Barangay 1', 'Barangay 2', 'Barangay 3', 'San Isidro', 'Santa Cruz', 'Santo Niño', 'Poblacion', 'San Antonio', 'Bagong Silang', 'Kamuning']

# Concern titles and descriptions by category
CONCERN_TEMPLATES = {
    'FLOOD': [
        ('Flooding in main street', 'The main street has been flooded for 3 days now. Water level is knee-high and blocking traffic.'),
        ('Canal overflow near market', 'The drainage canal near the public market is overflowing causing health concerns.'),
        ('Flash flood during heavy rain', 'Every time it rains heavily, our street gets flooded within 30 minutes.'),
    ],
    'ROAD': [
        ('Pothole causing accidents', 'There is a large pothole on the highway that has caused multiple accidents.'),
        ('Road needs repaving', 'The road in our subdivision has deteriorated badly and needs immediate repair.'),
        ('Missing road signs', 'Several road signs have been removed/stolen and are not being replaced.'),
    ],
    'WASTE': [
        ('Garbage not collected for weeks', 'Our area has not had garbage collection for 2 weeks now.'),
        ('Illegal dumping site', 'Someone is using the vacant lot as an illegal dumping site.'),
        ('Need more trash bins in park', 'The public park needs more trash bins as litter is everywhere.'),
    ],
    'ELECTRICITY': [
        ('Frequent power outages', 'We experience power outages almost every day lasting 2-3 hours.'),
        ('Broken street lights', 'Multiple street lights in our area are not working for months now.'),
        ('Exposed electrical wires', 'There are exposed electrical wires near the school that are dangerous.'),
    ],
    'WATER': [
        ('No water supply for days', 'Our area has had no water supply for 4 days now.'),
        ('Low water pressure', 'The water pressure in our area is very low, especially during mornings.'),
        ('Dirty water from tap', 'The tap water has been yellowish/brownish and smells bad.'),
    ],
    'SAFETY': [
        ('Street crime increasing', 'There have been multiple robbery incidents in our area recently.'),
        ('Stray dogs everywhere', 'Stray dogs are becoming a problem and some have attacked residents.'),
        ('Illegal parking blocking roads', 'Vehicles are illegally parked blocking emergency vehicle access.'),
    ],
    'OTHER': [
        ('Noise pollution from construction', 'Construction site operates even at night causing noise pollution.'),
        ('Need pedestrian crossing', 'We need a pedestrian crossing near the school for student safety.'),
        ('Abandoned building attracting vagrants', 'The abandoned building is being used by vagrants and is unsafe.'),
    ],
}

COMMENT_TEMPLATES = [
    'I am also experiencing this issue in our area.',
    'This has been going on for months now. Please address this urgently.',
    'Thank you for reporting this. I hope the barangay takes action soon.',
    'Same problem here in our street. Very frustrating.',
    'I have reported this before but nothing happened.',
    'The barangay officials said they will look into this.',
    'This is a safety hazard. Please prioritize this.',
    'We need to follow up on this issue regularly.',
    'Has anyone contacted the municipal office about this?',
    'I can confirm this issue. Seen it myself.',
    'This affects many families in our area.',
    'LGU should allocate budget for this.',
    'We filed a similar complaint last year.',
    'Please include photos next time for documentation.',
    'The situation is getting worse every week.',
]

FILIPINO_FIRST_NAMES = ['Juan', 'Maria', 'Jose', 'Ana', 'Pedro', 'Rosa', 'Ramon', 'Luz', 'Antonio', 'Carmen', 'Francisco', 'Elena', 'Miguel', 'Isabel', 'Ricardo', 'Teresa', 'Roberto', 'Gloria', 'Eduardo', 'Fe']
FILIPINO_LAST_NAMES = ['Santos', 'Reyes', 'Cruz', 'Bautista', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Gonzales', 'Ramos', 'Villanueva', 'Castro', 'Dela Cruz', 'Fernandez', 'Lopez']

def random_alias():
    adjectives = ['Quick', 'Bright', 'Calm', 'Eager', 'Fair', 'Gentle', 'Happy', 'Jolly', 'Kind', 'Noble', 'Proud', 'Quiet', 'Sharp', 'Swift', 'Wise', 'Bold', 'Cool', 'Neat']
    nouns = ['Pinoy', 'Kabayan', 'Citizen', 'Resident', 'Neighbor', 'Voter', 'Advocate', 'Observer', 'Reporter', 'Member']
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 999)}"

print("=" * 50)
print("SEEDING PRODUCTION DATABASE")
print("=" * 50)

# ========== CREATE USERS ==========
print("\n[1/5] Creating users...")
users = []

# Ensure admin exists
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@barangayconnect.ph',
        'role': 'ADMIN',
        'is_staff': True,
        'is_superuser': True,
        'alias': 'SystemAdmin',
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"  Created admin: admin / admin123")
else:
    print(f"  Admin already exists")

# Ensure LGU staff exists
lgu, created = User.objects.get_or_create(
    username='lgu_staff',
    defaults={
        'email': 'lgu@barangayconnect.ph',
        'role': 'LGU',
        'is_staff': True,
        'alias': 'LGUOfficial',
        'first_name': 'LGU',
        'last_name': 'Staff',
    }
)
if created:
    lgu.set_password('lgu123')
    lgu.save()
    print(f"  Created LGU: lgu_staff / lgu123")
else:
    print(f"  LGU staff already exists")

users.append(admin)
users.append(lgu)

# Create regular users
for i in range(NUM_USERS):
    first_name = random.choice(FILIPINO_FIRST_NAMES)
    last_name = random.choice(FILIPINO_LAST_NAMES)
    username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 99)}"
    
    if User.objects.filter(username=username).exists():
        continue
    
    region = random.choice(REGIONS)
    province = random.choice(PROVINCES.get(region, ['Unknown']))
    
    user = User.objects.create_user(
        username=username,
        email=f"{username}@email.com",
        password='password123',
        first_name=first_name,
        last_name=last_name,
        alias=random_alias(),
        barangay=random.choice(BARANGAYS),
        municipality=random.choice(MUNICIPALITIES),
        province=province,
        region=region,
        points=random.randint(-3, 10),
    )
    users.append(user)
    print(f"  Created user: {username}")

print(f"  Total users: {len(users)}")

# ========== CREATE CONCERNS ==========
print("\n[2/5] Creating concerns...")
concerns = []
statuses = ['PENDING', 'PENDING', 'PENDING', 'IN_PROGRESS', 'IN_PROGRESS', 'RESOLVED']
priorities = ['LOW', 'MEDIUM', 'MEDIUM', 'HIGH', 'URGENT']

for i in range(NUM_CONCERNS):
    category = random.choice(list(CONCERN_TEMPLATES.keys()))
    title, description = random.choice(CONCERN_TEMPLATES[category])
    
    # Add some variation to titles
    title = f"{title} - {random.choice(BARANGAYS)}"
    
    reporter = random.choice(users[2:]) if len(users) > 2 else users[0]
    region = random.choice(REGIONS)
    province = random.choice(PROVINCES.get(region, ['Unknown']))
    
    concern = Concern.objects.create(
        title=title,
        description=description + f"\n\nReported from {random.choice(BARANGAYS)}, {random.choice(MUNICIPALITIES)}.",
        category=category,
        status=random.choice(statuses),
        priority=random.choice(priorities),
        location=f"{random.choice(BARANGAYS)}, {random.choice(MUNICIPALITIES)}",
        barangay=random.choice(BARANGAYS),
        municipality=random.choice(MUNICIPALITIES),
        province=province,
        region=region,
        reporter=reporter,
        is_anonymous=random.choice([True, False, False]),  # 33% anonymous
        latitude=14.5 + random.uniform(-0.2, 0.2),  # Around Metro Manila
        longitude=121.0 + random.uniform(-0.2, 0.2),
        created_at=timezone.now() - timedelta(days=random.randint(1, 30)),
    )
    concerns.append(concern)
    print(f"  Created concern: {concern.title[:40]}...")

print(f"  Total concerns: {len(concerns)}")

# ========== CREATE COMMENTS ==========
print("\n[3/5] Creating comments...")
comments = []

for concern in concerns:
    num_comments = random.randint(*COMMENTS_PER_CONCERN)
    for _ in range(num_comments):
        author = random.choice(users)
        comment = Comment.objects.create(
            concern=concern,
            author=author,
            content=random.choice(COMMENT_TEMPLATES),
            created_at=concern.created_at + timedelta(hours=random.randint(1, 72)),
        )
        comments.append(comment)

print(f"  Total comments: {len(comments)}")

# ========== CREATE VOTES ==========
print("\n[4/5] Creating votes...")
vote_count = 0

for concern in concerns:
    num_votes = random.randint(0, 8)
    voters = random.sample(users, min(num_votes, len(users)))
    
    for voter in voters:
        if voter == concern.reporter:
            continue
        
        if not Vote.objects.filter(voter=voter, concern=concern).exists():
            Vote.objects.create(
                voter=voter,
                concern=concern,
                value=random.choice([1, 1, 1, -1]),  # 75% upvotes
            )
            vote_count += 1

print(f"  Total votes: {vote_count}")

# ========== CREATE REPORTS ==========
print("\n[5/5] Creating comment reports...")

# Create a few pending reports for demo
sample_comments = random.sample(comments, min(5, len(comments)))
for comment in sample_comments:
    reporter = random.choice([u for u in users if u != comment.author])
    CommentReport.objects.get_or_create(
        comment=comment,
        reporter=reporter,
        defaults={
            'reason': random.choice([
                'This comment contains inappropriate language.',
                'This looks like spam.',
                'Offensive content that violates community guidelines.',
                'Harassing or bullying behavior.',
            ]),
            'status': 'PENDING',
        }
    )

print(f"  Created {min(5, len(comments))} sample reports")

# ========== SUMMARY ==========
print("\n" + "=" * 50)
print("SEEDING COMPLETE!")
print("=" * 50)
print(f"Users: {User.objects.count()}")
print(f"Concerns: {Concern.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
print(f"Votes: {Vote.objects.count()}")
print(f"Reports: {CommentReport.objects.count()}")
print("\nAdmin Login: admin / admin123")
print("LGU Login: lgu_staff / lgu123")
print("=" * 50)
