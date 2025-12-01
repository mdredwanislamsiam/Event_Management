import os
import django
from faker import Faker
import random
from events.models import Event, Participant, Category

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Management.settings')
django.setup()

# Function to populate the database


def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Projects
    categories = [Category.objects.create(
        category_name=fake.bs().capitalize()[:30],
        category_description=fake.paragraph(),
    ) for _ in range(5)]
    print(f"Created {len(categories)} categories")

    # Create Employees
    employees = [Participant.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]
    print(f"Created {len(employees)} employees.")

    # Create Tasks
    events = []
    for _ in range(20):
        event = Event.objects.create(
            category=random.choice(categories),
            name=fake.sentence()[:30],
            description=fake.paragraph(),
            date=fake.date_this_year(),
            time = fake.time(),
            location = fake.city()[:30],
        )
        event.participant.set(random.sample(employees, random.randint(1, 3)))
        events.append(event)
    print(f"Created {len(events)} events.")


    print("Populated TaskDetails for all tasks.")
    print("Database populated successfully!")