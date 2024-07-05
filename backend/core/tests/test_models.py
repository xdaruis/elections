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

  def test_new_user_email_normalized(self):
    """Should normalize user email"""
    emails = [
      ['test1@EXAMPLE.com', 'test1@example.com'],
      ['Test2@example.com', 'Test2@example.com'],
      ['TeSt3@eXaMpLe.cOm', 'TeSt3@example.com'],
      ['TEST4@EXAMPLE.COM', 'TEST4@example.com'],
      ['test5@example.COM', 'test5@example.com'],
    ]

    base = 'username'
    count = 1

    for email, expected in emails:
      username = f'{base}{count}'
      count += 1

      user = get_user_model().objects.create_user(username, email, 'password')
      self.assertEqual(user.email, expected)

  def test_creating_a_superuser(self):
    """Should create a superuser"""
    user = get_user_model().objects.create_superuser(
      'username',
      'test@example.com',
      'password'
    )
    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)
