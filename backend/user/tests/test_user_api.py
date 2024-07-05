from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import create_user

CREATE_USER_URL = reverse('user:create')


class PublicUserApiTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user_data = {
      'username': 'user',
      'name': 'User Tester',
      'email': 'user@example.com',
      'password': 'password',
    }

  def test_create_user_success(self):
    """Should create a user"""
    res = self.client.post(CREATE_USER_URL, self.user_data)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(username=self.user_data['username'])
    self.assertTrue(user.check_password(self.user_data['password']))
    self.assertNotIn('password', res.data)

  def test_user_with_existing_fields(self):
    """Should display bad request if username or email is taken"""
    create_user(**self.user_data)
    fields_to_test = ['username', 'email']

    for field in fields_to_test:
      payload = self.user_data.copy()
      if field == 'username':
        payload['email'] = 'new_user@example.com'
      else:
        payload['username'] = 'new_username'

      res = self.client.post(CREATE_USER_URL, payload)

      self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
      self.assertIn(f'user with this {field} already exists.', str(res.data))

  def test_password_too_short(self):
    """Shouldn't be able to have a password shorter than 8 characters"""
    payload = self.user_data.copy()
    payload['password'] = 'passwor'

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    user_exists = get_user_model().objects.filter(
      email=payload['username']
    ).exists()
    self.assertFalse(user_exists)