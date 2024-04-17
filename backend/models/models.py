import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# 通用公共的model写在这里
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
    verified_status = models.CharField(max_length=10, default='0')  # 0未审核 1审核通过 -1审核未通过


class User(AbstractUser):
    ROLE_CHOICES = (
        ('public', 'Public'),
        ('emergency_response_team', 'Emergency Response Team'),
        ('administrator', 'Administrator'),
    )

    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='public')
    # create_time = models.DateTimeField(default=datetime.datetime.now)


class Vehicle(models.Model):
    # Todo: 填充这里
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


class DrivingLocation(models.Model):
    # username = models.CharField(max_length=255)
    # latitude = models.FloatField()
    # longitude = models.FloatField()
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)
    # is_disabled = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="locations")

    # Defining latitude and longitude fields for 5 locations
    lat1 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon1 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time1 = models.DateTimeField(null=True, blank=True)

    lat2 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon2 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time2 = models.DateTimeField(null=True, blank=True)

    lat3 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon3 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time3 = models.DateTimeField(null=True, blank=True)

    lat4 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon4 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time4 = models.DateTimeField(null=True, blank=True)

    lat5 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon5 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time5 = models.DateTimeField(null=True, blank=True)

    lat6 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon6 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time6 = models.DateTimeField(null=True, blank=True)

    lat7 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon7 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time7 = models.DateTimeField(null=True, blank=True)

    lat8 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon8 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time8 = models.DateTimeField(null=True, blank=True)

    lat9 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon9 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time9 = models.DateTimeField(null=True, blank=True)

    lat10 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon10 = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    time10 = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Locations for {self.user.username}"

