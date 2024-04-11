import os
import django
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
django.setup()


import random
import string

from django.utils import timezone
from models.models import DrivingLocation


def generate_fake_data():
    print("Generating fake data")
    for _ in range(100):  # 生成100条假数据
        location = DrivingLocation()
        location.username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  # 生成一个随机的10位用户名
        location.latitude = random.uniform(-90, 90)  # 生成一个随机的纬度
        location.longitude = random.uniform(-180, 180)  # 生成一个随机的经度
        location.is_disabled = False
        location.save()
    print("Generated 100 fake DrivingLocation objects")

generate_fake_data()