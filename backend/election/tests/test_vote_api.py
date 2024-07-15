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
  create_vote
)
from core.models import Vote


class PrivateVoteApiTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = create_user()
    self.client.force_authenticate(user=self.user)

    self.election = create_election(
      start_date=timezone.now().date() - timedelta(days=1),
      end_date=timezone.now().date() + timedelta(days=7)
    )

    self.candidate1_user = create_user()
    self.candidate2_user = create_user()
    self.candidate1 = create_candidate(self.candidate1_user, self.election)
    self.candidate2 = create_candidate(self.candidate2_user, self.election)

  def test_create_vote(self):
    """Should create a vote successfully"""
    url = reverse('election:election-vote', args=[self.election.slug])
    payload = {'candidate_username': self.candidate1_user.username}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertTrue(Vote.objects.filter(
      user=self.user, election=self.election, voted_candidate=self.candidate1
    ).exists())

  def test_update_vote(self):
    create_vote(self.user, self.election, self.candidate1)
    url = reverse('election:election-vote', args=[self.election.slug])
    payload = {'candidate_username': self.candidate2_user.username}
    res = self.client.patch(url, payload)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertTrue(Vote.objects.filter(
      user=self.user, election=self.election, voted_candidate=self.candidate2
    ).exists())

  def test_delete_vote(self):
    create_vote(self.user, self.election, self.candidate1)
    url = reverse('election:election-vote', args=[self.election.slug])
    res = self.client.delete(url)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertFalse(Vote.objects.filter(
      user=self.user, election=self.election
    ).exists())

  def test_vote_inactive_election(self):
    past_election = create_election(
      start_date=timezone.now().date() - timedelta(days=14),
      end_date=timezone.now().date() - timedelta(days=7)
    )
    url = reverse('election:election-vote', args=[past_election.slug])
    payload = {'candidate_username': self.candidate1_user.username}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

  def test_vote_twice(self):
    create_vote(self.user, self.election, self.candidate1)
    url = reverse('election:election-vote', args=[self.election.slug])
    payload = {'candidate_username': self.candidate2_user.username}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_update_nonexistent_vote(self):
    url = reverse('election:election-vote', args=[self.election.slug])
    payload = {'candidate_username': self.candidate1_user.username}
    res = self.client.patch(url, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_delete_nonexistent_vote(self):
    url = reverse('election:election-vote', args=[self.election.slug])
    res = self.client.delete(url)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_vote_for_nonexistent_candidate(self):
    url = reverse('election:election-vote', args=[self.election.slug])
    payload = {'candidate_username': 'nonexistent_candidate'}
    res = self.client.post(url, payload)

    self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
