from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from core.tests.helpers import (
  create_candidate,
  create_election,
  create_user,
  create_vote,
)
from core.models import Candidate


class PublicCandidateApiTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user1 = create_user()
    self.user2 = create_user()

    self.election = create_election()
    self.candidate1 = create_candidate(self.user1, self.election)
    self.candidate2 = create_candidate(self.user2, self.election)
    self.candidate3 = create_candidate(create_user(), create_election())

  def test_list_candidates(self):
    """Should return a list of candidates"""
    url = reverse('election:election-candidates', args=[self.election.slug])
    res = self.client.get(url)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 2)

    # Check if both usernames are in the response
    usernames = [candidate['username'] for candidate in res.data]
    self.assertIn(self.user1.username, usernames)
    self.assertIn(self.user2.username, usernames)

    # Check that the third user's username is not in the response
    self.assertNotIn(self.candidate3.user.username, usernames)

  def test_votes_count(self):
    """Should return the list in descending order based on votes"""
    for _ in range(5):
      create_vote(create_user(), self.election, self.candidate2)

    for _ in range(3):
      create_vote(create_user(), self.election, self.candidate1)

    for _ in range(5):
      user = create_user()
      election = create_election()
      create_vote(user, election, create_candidate(user, election))

    url = reverse('election:election-candidates', args=[self.election.slug])
    res = self.client.get(url)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 2)

    # Check that the candidate with most votes is first
    self.assertEqual(res.data[0]['votes'], 5)
    self.assertEqual(res.data[0]['username'], self.user2.username)
    self.assertEqual(res.data[1]['votes'], 3)
    self.assertEqual(res.data[1]['username'], self.user1.username)


class PrivateCandidateApiTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = create_user()
    self.client.force_authenticate(user=self.user)

    self.election = create_election(
      start_date=timezone.now().date() + timedelta(days=7),
      end_date=timezone.now().date() + timedelta(days=14)
    )

  def test_create_candidate(self):
    url = reverse('election:election-candidate', args=[self.election.slug])
    payload = {'description': 'Test candidate description'}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertTrue(Candidate.objects.filter(
      user=self.user, election=self.election
    ).exists())

  def test_update_candidate(self):
    candidate = create_candidate(self.user, self.election)
    url = reverse('election:election-candidate', args=[self.election.slug])
    payload = {'description': 'Updated description'}
    res = self.client.patch(url, payload)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    candidate.refresh_from_db()
    self.assertEqual(candidate.description, 'Updated description')

  def test_delete_candidate(self):
    create_candidate(self.user, self.election)
    url = reverse('election:election-candidate', args=[self.election.slug])
    res = self.client.delete(url)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertFalse(Candidate.objects.filter(
      user=self.user, election=self.election
    ).exists())

  def test_create_candidate_already_exists(self):
    create_candidate(self.user, self.election)
    url = reverse('election:election-candidate', args=[self.election.slug])
    payload = {'description': 'Test candidate description'}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_nonexistent_candidate(self):
    url = reverse('election:election-candidate', args=[self.election.slug])
    payload = {'description': 'Updated description'}
    res = self.client.patch(url, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_delete_nonexistent_candidate(self):
    url = reverse('election:election-candidate', args=[self.election.slug])
    res = self.client.delete(url)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_candidate_actions_for_ongoing_election(self):
    ongoing_election = create_election(
      start_date=timezone.now().date() - timedelta(days=1),
      end_date=timezone.now().date() + timedelta(days=6)
    )
    url = reverse('election:election-candidate', args=[ongoing_election.slug])
    payload = {'description': 'Test candidate description'}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)