import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

#通用公共的model写在这里
# Create your models here.
class Disaster(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('public', 'Public'),
        ('emergency_response_team', 'Emergency Response Team'),
        ('administrator', 'Administrator'),
    )

    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='public')
    # create_time = models.DateTimeField(default=datetime.datetime.now)


class Vehicle(models.Model):
    #Todo: 填充这里
    vehicleId = models.CharField(max_length=16, unique=True)
    vehicleType = models.CharField(max_length=255)
