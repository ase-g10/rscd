from django.db import models

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


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    status = models.SmallIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)
    github_username = models.CharField(max_length=255, unique=True, null=True, blank=True)

class Vehicle(models.Model):
    #Todo: 填充这里
    vehicleId = models.CharField(max_length=16, unique=True)
    vehicleType = models.CharField(max_length=255)