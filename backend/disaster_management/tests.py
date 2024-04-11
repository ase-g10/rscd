from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models.models import Disaster
import json
from django.contrib.auth.models import User

class DisasterViewTests(APITestCase):

    def setUp(self):
        Disaster.objects.create(name="Test Disaster", description="A test disaster", latitude=1.0, longitude=2.0, location="Test Location", radius=100.0, type="Test Type", contact="Test Contact", image_url="http://example.com/image.jpg", verified_status="1")

    def test_post_location(self):
        url = '/dm/disasterview/post_location/'
        data = {'name': 'New Disaster', 'description': 'Description', 'latitude': '10.0', 'longitude': '20.0', 'location': 'New Location', 'radius': '150.0', 'type': 'Type', 'contact': 'Contact', 'imageUrl': 'http://example.com/newimage.jpg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Disaster.objects.count(), 2)
        self.assertEqual(Disaster.objects.get(name='New Disaster').location, 'New Location')
        print("dm: post_location pass")


    def test_read_all_verified(self):
        url = '/dm/disasterview/read_all_verified/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_data['message']), 1)
        print('dm: read_all_verified pass')

    def test_read_all_ongoing(self):
        url = '/dm/disasterview/read_all_ongoing/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('message', response_data)
        print("dm: read_all_ongoing pass")

    def test_read_all_verifying(self):
        url = '/dm/disasterview/read_all_verifying/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('message', response_data)
        print("dm: read_all_verifying pass")

    def test_calculate_safePoint(self):
        Disaster.objects.create(
            name="Test Disaster",
            description="A test disaster",
            latitude=10.1,
            longitude=20.1,
            location="Test Location",
            radius=100.0,  # Ensure this radius covers the test user's location
            type="Test Type",
            contact="Test Contact",
            image_url="http://example.com/image.jpg",
            verified_status="1"
        )
        url = '/dm/disasterview/calculate_safePoint/'  # Adjust based on actual URL pattern
        data = {'latitude': '10.0', 'longitude': '20.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))

        # Since a disaster overlaps with the user's location, we now expect 'safe_lat' and 'safe_lng' in the response
        self.assertIn('safe_lat', response_data)
        self.assertIn('safe_lng', response_data)
        print("dm: calculate_safePoint pass")


    def test_disaster_modify_write(self):
        url = '/dm/disastermodify/write/'  # Adjust based on actual URL pattern and action name
        data = {'key': 'value'}  # Adjust based on what data your action expects
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], {'key': 'value'})
        print("dm: write pass")

