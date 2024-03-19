from datetime import datetime
import os
import django
from faker import Faker
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


from models.models import Disaster


fake = Faker()

disaster_types = ['car_accident', 'fire', 'riot']
verification_status = ['0']


def create_disasters(n):
    for _ in range(n):
        name = fake.word().capitalize()
        description = fake.text(max_nb_chars=200)
        latitude = str(fake.latitude())
        longitude = str(fake.longitude())
        disaster_type = random.choice(disaster_types)
        is_verified = random.choice(verification_status)
        location = fake.address()


        disaster = Disaster(
            name=name,
            description=description,
            latitude=latitude,
            longitude=longitude,
            type=disaster_type,
            is_verified=is_verified,
            location=location,
            create_time=datetime.now(),
            update_time=datetime.now(),
            is_delete=False
        )
        disaster.save()


create_disasters(10)