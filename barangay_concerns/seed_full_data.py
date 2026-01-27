import os
import django
import random
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.concerns.models import Concern, Comment, Vote

User = get_user_model()

# --- CONSTANTS ---
BARANGAYS = [
    "Poblacion", "Banga", "Parulan", "Sto. Nino", "Sipat", 
    "Dampol", "Bintog", "San Jose", "Sta. Ines", "Agnaya",
    "Tabang", "Lumang Bayan", "Bagong Silang"
]

CATEGORIES = ['FLOOD', 'ROAD', 'WASTE', 'ELECTRICITY', 'WATER', 'SAFETY', 'OTHER']

TITLES = {
    'FLOOD': ["Deep flooding in street", "Canal clogged causing overflow", "Rising water level near creek", "Impassable road due to flood"],
    'ROAD': ["Deep pothole causing accidents", "Unfinished road construction", "Damaged sidewalk", "Missing manhole cover"],
    'WASTE': ["Garbage not collected for weeks", "Illegal dumping site", "Burning of trash in residential area", "Scattered debris on highway"],
    'ELECTRICITY': ["Streetlight busting", "Leaning electric post", "Power outage in area", "Sparking transformer"],
    'WATER': ["No water supply", "Dirty tap water", "Leaking main pipe", "Low water pressure"],
    'SAFETY': ["Suspicious individuals at night", "Stray dogs chasing kids", "Loud videoke past curfew", "Robbery incident reported"],
    'OTHER': ["Lost dog found", "Community pantry donation", "Tree branch blocking view", "Request for fogging"]
}

# Center around Plaridel
BASE_LAT = 14.892
BASE_LNG = 120.875

def clean_db():
    print("Cleaning database...")
    Vote.objects.all().delete()
    Comment.objects.all().delete()
    Concern.objects.all().delete()
    User.objects.exclude(is_superuser=True).exclude(username='admin').delete()

def create_users():
    print("Creating users...")
    users = []
    
    # 1. LGU Staff
    lgu = User.objects.create_user(username='lgu_staff', email='lgu@plaridel.gov.ph', password='password123')
    lgu.role = 'LGU'
    lgu.first_name = "Office of the"
    lgu.last_name = "Mayor"
    lgu.alias = "LGU Admin"
    lgu.save()
    users.append(lgu)
    
    # 2. Good Citizens (High Karma)
    good_names = ['JuanDelaCruz', 'MariaClara', 'JoseRizal', 'AndresBoni', 'GabrielaS']
    for name in good_names:
        u = User.objects.create_user(username=name.lower(), email=f'{name.lower()}@gmail.com', password='password123')
        u.role = 'USER'
        u.first_name = name
        u.alias = name
        u.points = random.randint(50, 500)
        u.barangay = random.choice(BARANGAYS)
        u.save()
        users.append(u)
        
    # 3. Regular Users (Neutral)
    reg_names = ['worker1', 'student2', 'driver3', 'mommy4', 'tito5']
    for name in reg_names:
        u = User.objects.create_user(username=name, email=f'{name}@yahoo.com', password='password123')
        u.role = 'USER'
        u.alias = f"Citizen {name[-1]}"
        u.points = random.randint(0, 50)
        u.barangay = random.choice(BARANGAYS)
        u.save()
        users.append(u)
        
    # 4. Trolls / Low Karma
    troll_names = ['troll_face', 'spammer_xd', 'hater101']
    for name in troll_names:
        u = User.objects.create_user(username=name, email=f'{name}@fake.com', password='password123')
        u.role = 'USER'
        u.alias = name
        u.points = random.randint(-100, -5)
        if u.points < -50:
            u.is_flagged_for_legal_action = True
            u.legal_action_reason = "Repeated false reports and harassment."
        u.save()
        users.append(u)
        
    return users

def create_concerns(users):
    print("Creating concerns...")
    concerns = []
    
    for i in range(50):
        cat = random.choice(CATEGORIES)
        status = random.choice(['PENDING', 'PENDING', 'PENDING', 'IN_PROGRESS', 'RESOLVED'])
        reporter = random.choice(users)
        
        # Random location shift
        lat = BASE_LAT + random.uniform(-0.02, 0.02)
        lng = BASE_LNG + random.uniform(-0.02, 0.02)
        
        c = Concern.objects.create(
            title=random.choice(TITLES[cat]),
            description=f"Located near {random.choice(['the church', 'the school', 'the store', 'block 5'])}. Please assist immediately. {random.choice(['Impacts traffic.', 'Smells bad.', 'Very dangerous.', 'Need help.'])}",
            category=cat,
            location=f"Street {random.randint(1,20)}",
            barangay=random.choice(BARANGAYS),
            municipality="Plaridel",
            latitude=lat,
            longitude=lng,
            status=status,
            priority=random.choice(['LOW', 'MEDIUM', 'HIGH']),
            reporter=reporter,
            is_anonymous=random.choice([True, False, False, False]),
            created_at=timezone.now() - datetime.timedelta(days=random.randint(0, 30))
        )
        
        # If resolved, set resolved_at
        if status == 'RESOLVED':
            c.resolved_at = c.created_at + datetime.timedelta(days=random.randint(1, 5))
            c.save()
            
        concerns.append(c)
        
    return concerns

def create_interactions(users, concerns):
    print("Creating comments and votes...")
    
    comments_text = [
        "I saw this too!", "Hope this gets fixed soon.", "Calling LGU attention.",
        "Any update on this?", "This has been here for months!", "Thank you for reporting.",
        "Ingat po kayo.", "Already reported this last week."
    ]
    
    for c in concerns:
        # Votes
        num_votes = random.randint(0, 10)
        potential_voters = list(users)
        random.shuffle(potential_voters)
        
        for v in range(min(num_votes, len(potential_voters))):
            voter = potential_voters[v]
            if voter == c.reporter: continue 
            
            val = 1
            # Trolls mostly downvote, good guys mostly upvote, randoms mixed
            if "troll" in voter.username:
                val = -1
            elif c.status == 'RESOLVED':
                val = 1
            else:
                val = random.choice([1, 1, 1, -1])
            
            try:
                Vote.objects.create(voter=voter, concern=c, value=val)
                # Update reporter points
                if c.reporter:
                    c.reporter.points += val
                    c.reporter.save()
            except:
                pass

        # Comments
        num_comments = random.randint(0, 5)
        for _ in range(num_comments):
            author = random.choice(users)
            Comment.objects.create(
                concern=c,
                author=author,
                content=random.choice(comments_text)
            )

if __name__ == '__main__':
    clean_db()
    users = create_users()
    concerns = create_concerns(users)
    create_interactions(users, concerns)
    print("Seeding complete!")
