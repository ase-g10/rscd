import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

#通用公共的model写在这里
# Create your models here.
class Disaster(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=40, default='Car Accident')
    radius = models.FloatField(default=0)
    description = models.TextField(blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    image_url = models.CharField(max_length=255, default="")
    contact = models.CharField(max_length=255, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_onging = models.BooleanField(default=True)
    verified_status = models.CharField(max_length=10, default='0') #0未审核 1审核通过 -1审核未通过


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


class Log(models.Model):
    disaster_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    radius = models.FloatField(default=0.0)
    type = models.CharField(max_length=40, default="")
    image_url = models.CharField(max_length=255, default="")
    create_time = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    responsible_team = models.CharField(max_length=255)
