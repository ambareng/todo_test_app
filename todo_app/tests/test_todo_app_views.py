import datetime
import jwt
import pytest

from django.test import TestCase
from django.contrib.auth.models import User

from mixer.backend.django import mixer

from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from todo_app.models import Todo, TodoList


class TestTodoAppViews(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = mixer.blend(User)
        self.admin = mixer.blend(User, is_superuser=True)

        self.key = 'secret'
        self.user_payload = {
            'id': self.user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        self.admin_payload = {
            'id': self.admin.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        encoded = jwt.encode(self.user_payload, self.key, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + encoded)

    def test_todo_lists_api_view_get(self):
        url = reverse('todo_lists')
        todo_list = mixer.blend(TodoList, name='Sample Todo List', user=self.user)
        todo_list_02 = mixer.blend(TodoList, name='Admin Todo List', user=self.admin)
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 1
        assert response.json()[0].get('name') == todo_list.name

        # FOR ADMIN USERS TEST
        encoded = jwt.encode(self.admin_payload, self.key, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + encoded)
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.json() is not None
        assert len(response.json()) == 2

    def test_todo_lists_api_view_post(self):
        todo_lists_data = {
            "name": "Sample Todo List"
        }
        url = reverse('todo_lists')
        response = self.client.post(url, todo_lists_data)

        assert response.status_code == 200
        assert response.json() is not None
        assert response.json().get('name') == todo_lists_data.get('name')

        invalid_todo_lists_data = {
            "invalid": "invalid"
        }

        response = self.client.post(url, invalid_todo_lists_data)

        assert response.json().get('name') == ['This field is required.']

    def test_todo_list_details_api_view_get(self):
        todo_list = mixer.blend(TodoList, name='Sample Todo List', user=self.user)
        url = reverse('todo_list_details', args=[todo_list.id])
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.json() is not None
        assert response.json().get('name') == todo_list.name

        # FOR ADMIN USERS
        encoded = jwt.encode(self.admin_payload, self.key, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + encoded)
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.json() is not None
        assert response.json().get('name') == todo_list.name

    def test_todo_list_details_api_view_put(self):
        todo_lists_data = {
            "name": "Sample Todo List"
        }
        todo_list = mixer.blend(TodoList, user=self.user)
        url = reverse('todo_list_details', args=[todo_list.id])
        response = self.client.put(url, todo_lists_data)

        assert response.status_code == 200
        assert response.json().get('name') == 'Sample Todo List'

        # FOR ADMIN USERS
        todo_lists_data = {
            "name": "Sample Todo List (Edited)"
        }

        encoded = jwt.encode(self.admin_payload, self.key, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + encoded)
        response = self.client.put(url, todo_lists_data)

        assert response.json().get('name') == 'Sample Todo List (Edited)'

        # FOR SERIALIZER ERROR
        invalid_todo_list_data = {
            "invalid": "invalid"
        }

        encoded = jwt.encode(self.admin_payload, self.key, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + encoded)
        response = self.client.put(url, invalid_todo_list_data)

        assert response.json().get('name') == ['This field is required.']

    def test_todo_list_details_api_view_delete(self):
        todo_list = mixer.blend(TodoList, user=self.user)
        url = reverse('todo_list_details', args=[todo_list.id])
        response = self.client.delete(url)

        assert response.status_code == 204
        assert TodoList.objects.count() == 0

        # FOR ADMIN USERS
        todo_list = mixer.blend(TodoList, user=self.user)
        url = reverse('todo_list_details', args=[todo_list.id])
        encoded = jwt.encode(self.admin_payload, self.key, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + encoded)
        response = self.client.delete(url)

        assert response.status_code == 204
        assert TodoList.objects.count() == 0
