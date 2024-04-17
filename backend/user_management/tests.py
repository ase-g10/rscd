from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from models.models import User
from django.conf import settings


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        self.register_url = '/um/auth/register/'
        self.login_url = '/um/auth/login/'
        self.logout_url = '/um/auth/logout/'

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print('um: register_user_success pass')
        # self.assertIn('User created successfully', response.data['message'])

    def test_register_user_failure(self):
        # Create a user first to trigger a duplicate entry
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('um: register_user_failure pass')

    def test_login_user_success(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('access_token', response.data)
        print('um: login_user_success pass')

    def test_login_user_failure(self):
        response = self.client.post(self.login_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('um: login_user_failure pass')

    def test_logout_user(self):
        # Assuming user is logged in
        self.client.force_authenticate(user=User.objects.create_user(**self.user_data))
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('um: logout_user pass')


class UserInfoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_info_url = '/um/user_info/get_user_info/'
        self.user = User.objects.create_user(username='testuser', email='test@example.com',
                                             password='securepassword123')

    def test_get_user_info_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print('um: get_user_info_authenticated pass')

    def test_get_user_info_unauthenticated(self):
        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('um: get_user_info_unauthenticated pass')
