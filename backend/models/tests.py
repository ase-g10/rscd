from django.test import TestCase
from .models import Disaster, User, Vehicle, Log, DrivingLocation
from django.contrib.auth import get_user_model
import datetime

class ModelTests(TestCase):
    def test_create_disaster(self):
        name = "Earthquake"
        disaster = Disaster.objects.create(
            name=name,
            type="Natural",
            radius=10.0,
            description="A severe earthquake",
            latitude="34.0522",
            longitude="-118.2437",
            location="Los Angeles",
            contact="emergency_services",
        )
        self.assertEqual(disaster.name, name)
        self.assertTrue(disaster.is_onging)
        print("models: disaster pass")

    def test_create_user(self):
        username = "testuser"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            role="public",
        )
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, "public")
        print("models: user pass")

    def test_create_vehicle(self):
        """Test creating a vehicle is successful."""
        vehicleId = "XYZ123"
        vehicleType = "Car"
        vehicle = Vehicle.objects.create(
            vehicleId=vehicleId,
            vehicleType=vehicleType,
        )
        self.assertEqual(vehicle.vehicleId, vehicleId)
        self.assertEqual(vehicle.vehicleType, vehicleType)
        print("models: vehicle pass")

    def test_create_log(self):
        disaster_name = "Flood"
        description = "A severe flood"
        log = Log.objects.create(
            disaster_name=disaster_name,
            description=description,
            latitude="40.7128",
            longitude="-74.0060",
            location="New York",
            radius=5.0,
            type="Natural",
            create_time="2023-04-12",
            responsible_team="NY Emergency Services",
        )
        self.assertEqual(log.disaster_name, disaster_name)
        self.assertEqual(log.description, description)
        print("models: log pass")

    def test_create_driving_location(self):
        user = get_user_model().objects.create_user(username="testdriver", password="testpass123")
        latitude = 34.0522
        longitude = -118.2437
        driving_location = DrivingLocation.objects.create(
            user=user,
            lat10=latitude,
            lon10=longitude,
        )
        self.assertEqual(driving_location.user, user)
        self.assertEqual(driving_location.lat10, latitude)
        self.assertEqual(driving_location.lon10, longitude)
        print("models: driving_location pass")

