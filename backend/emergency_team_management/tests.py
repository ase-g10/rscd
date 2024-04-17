from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from models.models import Disaster, Log
import json

class EmergencyViewTests(APITestCase):
    def setUp(self):
        Disaster.objects.create(
            name="Test Disaster",
            description="A test disaster scenario",
            latitude="10.0",
            longitude="20.0",
            location="Test Location",
            is_onging=True,
            type="Natural",
            radius=100.0,
            create_time="2022-04-12T23:20:50.52Z"
        )
        Log.objects.create(
            disaster_name="Test Disaster",
            description="A test disaster scenario",
            latitude="10.0",
            longitude="20.0",
            location="Test Location",
            responsible_team="responsible_team",
            radius=100.0,
            type="Natural",
            create_time="2022-04-12T23:20:50.52Z"
        )

    def test_response_action(self):
        url = '/etm/emergencyview/response/'
        data = {
            'name': 'Test Disaster',
            'description': 'A test disaster scenario ended',
            'latitude': '10.0',
            'longitude': '20.0',
            'location': 'Test Location',
            'username': 'responsible_team'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['message'], "Successful!")
        self.assertFalse(Disaster.objects.filter(latitude='10.0', longitude='20.0', is_onging=True).exists())
        self.assertTrue(Log.objects.filter(disaster_name='Test Disaster').exists())
        print("etm: response pass")

    def test_read_all_logs(self):
        url = '/etm/emergencyview/read_all_logs/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(json.loads(response.content)['message']) > 0)
        print("etm: read_all_logs pass")

    def test_read_specific_log(self):
        url = '/etm/emergencyview/read_specific_log/'
        response = self.client.get(url, {'disaster_id': '1'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        print("etm: read_specific_log pass")
