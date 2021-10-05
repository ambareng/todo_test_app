import pytest

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from mixer.backend.django import mixer

from rest_framework.test import APIClient
from rest_framework.reverse import reverse


class TestAuthViews(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login(self):
        user = mixer.blend(User, email='test@test.com', password=make_password('Yeahyeahyeah1!'))
        login_data = {
            "email": "test@test.com",
            "password": "Yeahyeahyeah1!"
        }
        url = reverse('login')
        response = self.client.post(url, login_data)

        assert 'Token' in response.json().get('jwt')

        # INVALID LOGIN CREDENTIALS
        invalid_login_data = {
            "email": "test@test.com",
            "password": "Yeahyeahyeah1"
        }
        url = reverse('login')
        response = self.client.post(url, invalid_login_data)

        assert response.json().get('error') == 'Invalid email or password'

    def test_register(self):
        register_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "Yeahyeahyeah1!"
        }
        url = reverse('register')
        response = self.client.post(url, register_data)

        assert response.json().get('email') == 'test@test.com'
        assert response.json().get('username') == 'test'
