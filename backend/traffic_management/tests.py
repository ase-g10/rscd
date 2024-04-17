from datetime import timezone
from random import random

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json
from models.models import DrivingLocation, User

class TrafficViewTests(APITestCase):
    def test_get_driving_location(self):
        url = '/tm/trafficview/get_driving_location/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content.decode('utf-8'))
        print(response_data)
        if 'locations' in response_data:
            # 在这里添加你对 'locations' 的断言
            pass
        else:
            self.assertEqual(response_data['status'], 'error')
            self.assertEqual(response_data['message'], 'No location data available.')
            print('tm: get_driving_location_no_data pass')
        print('tm: get_driving_location pass')

    def test_save_driving_location(self):
        url = '/tm/trafficview/save_driving_location/'
        data = {'username': 'test', 'latitude': '10.0', 'longitude': '20.0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('tm: save_driving_location pass')

