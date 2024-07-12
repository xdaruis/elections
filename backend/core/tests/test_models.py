from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from core import models
from core.tests.helpers import create_user, create_election, create_candidate


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

  def test_creating_a_candidate(self):
    """Should create a candidate"""
    user = create_user()
    election = create_election()
    payload = {
      'user': user,
      'election': election,
      'description': 'I will create a better future!',
    }
    candidate = models.Candidate.objects.create(**payload)
    self.assertEqual(str(candidate), f'{user.username} - {election.slug}')

  def test_creating_duplicate_candidate(self):
    """Should not create another candidate for the same user and election"""
    user = create_user()
    election = create_election()
    payload = {
      'user': user,
      'election': election,
      'description': 'I will create a better future!',
    }
    models.Candidate.objects.create(**payload)
    with self.assertRaises(IntegrityError):
      models.Candidate.objects.create(**payload)

  def test_creating_candidate_for_different_elections(self):
    """
    Should allow creating candidates for the same user in different elections
    """
    user = create_user()
    election1 = create_election()
    election2 = create_election()

    candidate1 = models.Candidate.objects.create(
      user=user,
      election=election1,
      description='Description for Election 1'
    )
    candidate2 = models.Candidate.objects.create(
      user=user,
      election=election2,
      description='Description for Election 2'
    )
    self.assertEqual(models.Candidate.objects.count(), 2)
    self.assertEqual(str(candidate1), f'{user.username} - {election1.slug}')
    self.assertEqual(str(candidate2), f'{user.username} - {election2.slug}')

  def test_creating_candidates_for_same_election(self):
    """
    Should allow creating candidates for different users in the same election
    """
    user1 = create_user()
    user2 = create_user()
    election = create_election()

    candidate1 = models.Candidate.objects.create(
      user=user1,
      election=election,
      description='Description for User 1'
    )
    candidate2 = models.Candidate.objects.create(
      user=user2,
      election=election,
      description='Description for User 2'
    )

    self.assertEqual(models.Candidate.objects.count(), 2)
    self.assertEqual(str(candidate1), f'{user1.username} - {election.slug}')
    self.assertEqual(str(candidate2), f'{user2.username} - {election.slug}')

  def test_create_vote(self):
    """Should create a vote successfully."""
    user = create_user()
    election = create_election()
    candidate = create_candidate(create_user(), election)

    vote = models.Vote.objects.create(
      user=user,
      election=election,
      voted_candidate=candidate
    )

    self.assertEqual(models.Vote.objects.count(), 1)
    self.assertEqual(
      str(vote),
      f'{user.username} voted in {election.title} for {candidate.user.username}'
    )

  def test_unique_vote_per_user_per_election(self):
    """Should not allow a user to vote twice in the same election."""
    user = create_user()
    election = create_election()
    candidate1 = create_candidate(create_user(), election)
    candidate2 = create_candidate(create_user(), election)

    models.Vote.objects.create(
      user=user,
      election=election,
      voted_candidate=candidate1
    )

    with self.assertRaises(ValidationError):
      models.Vote.objects.create(
        user=user,
        election=election,
        voted_candidate=candidate2
      )

  def test_user_can_vote_in_different_elections(self):
    """Should allow a user to vote in different elections."""
    user = create_user()
    election1 = create_election()
    election2 = create_election()
    candidate1 = create_candidate(create_user(), election1)
    candidate2 = create_candidate(create_user(), election2)

    vote1 = models.Vote.objects.create(
        user=user,
        election=election1,
        voted_candidate=candidate1
    )

    vote2 = models.Vote.objects.create(
        user=user,
        election=election2,
        voted_candidate=candidate2
    )

    self.assertEqual(models.Vote.objects.count(), 2)
    self.assertNotEqual(vote1.election, vote2.election)

  def test_vote_for_candidate_in_wrong_election(self):
    """Should not allow voting for a candidate in the wrong election."""
    user = create_user()
    election1 = create_election()
    election2 = create_election()
    candidate = create_candidate(create_user(), election1)

    with self.assertRaises(Exception):
      models.Vote.objects.create(
        user=user,
        election=election2,
        voted_candidate=candidate
      )

  def test_cascade_delete(self):
    """
    Should delete votes when related user, election, or candidate is deleted.
    """
    user = create_user()
    election = create_election()
    candidate = create_candidate(create_user(), election)

    models.Vote.objects.create(
      user=user,
      election=election,
      voted_candidate=candidate
    )

    self.assertEqual(models.Vote.objects.count(), 1)

    user.delete()
    self.assertEqual(models.Vote.objects.count(), 0)

    user = create_user()
    models.Vote.objects.create(
      user=user,
      election=election,
      voted_candidate=candidate
    )

    # Test cascade on election delete
    election.delete()
    self.assertEqual(models.Vote.objects.count(), 0)

    election = create_election()
    candidate = create_candidate(create_user(), election)

    models.Vote.objects.create(
      user=user,
      election=election,
      voted_candidate=candidate
    )

    # Test cascade on candidate delete
    candidate.delete()
    self.assertEqual(models.Vote.objects.count(), 0)
