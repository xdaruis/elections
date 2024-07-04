from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
  def test_create_user_successfull(self):
    """Should create an user"""
    username = 'username'
    email = 'test@example.com'
    password = 'password'
    user = get_user_model().objects.create_user(
      username=username,
      email=email,
      password=password,
    )

    self.assertEqual(user.username, username)
    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))
