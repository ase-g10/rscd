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
        print("post_location pass")


    def test_read_all_verified(self):
        url = '/dm/disasterview/read_all_verified/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_data['message']), 1)
        print('read_all_verified pass')

# Continue with tests for read_all_ongoing, read_all_verifying, calculate_safePoint, and the actions in DisasterModify

