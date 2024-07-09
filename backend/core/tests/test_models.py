from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from core import models


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

  def test_creating_an_election(self):
    """Should create an election"""
    payload = {
      'title': 'Election',
      'start_date': '2024-01-01',
      'end_date': '2024-01-02',
    }
    election = models.Election.objects.create(**payload)

    self.assertEqual(str(election), election.title)

  def test_creating_election_missing_fields(self):
    """Should throw an error if missing fields"""
    payload = {
      'title': 'Election',
      'start_date': '2024-01-01',
      'end_date': '2024-01-02',
    }
    for field in ['title', 'start_date', 'end_date']:
      wrong_payload = payload.copy()
      del wrong_payload[field]

      with self.assertRaises(ValidationError):
        models.Election.objects.create(**wrong_payload)

  def test_creating_election_with_wrong_dates(self):
    """Should throw an error if wrong dates"""
    payload = {
      'title': 'Election',
      'start_date': '2024-01-01',
      'end_date': '2024-01-02',
    }
    wrong_dates = ['2024-01-02', '2024-01-03', '2024.01.03']
    for date in wrong_dates:
      wrong_payload = payload.copy()
      wrong_payload['start_date'] = date

      with self.assertRaises(ValidationError):
        models.Election.objects.create(**wrong_payload)
