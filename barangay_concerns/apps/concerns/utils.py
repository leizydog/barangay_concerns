
import random
import string

ADJECTIVES = ['Concerned', 'Active', 'Helpful', 'Worried', 'Observant', 'Vigilant', 'Calm', 'Quick', 'Safe', 'Anonymous']
NOUNS = ['Neighbor', 'Citizen', 'Resident', 'Local', 'Reporter', 'Observer', 'Pinoy', 'Kababayan', 'Pedestrian', 'Driver']

def generate_random_alias():
    """Generates a random alias like 'ConcernedNeighbor88'."""
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    number = random.randint(10, 999)
    return f"{adj}{noun}{number}"
