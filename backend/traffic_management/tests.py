from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class TrafficViewTests(APITestCase):
    def test_get_driving_location(self):
        url = '/tm/trafficview/get_driving_location/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('locations', response_data)
        print('tm: get_driving_location pass')

    def test_save_driving_location(self):
        url = '/tm/trafficview/save_driving_location/'
        data = {'username': 'test', 'latitude': '10.0', 'longitude': '20.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('tm: save_driving_location pass')