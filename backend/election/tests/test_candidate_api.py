from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.tests.helpers import create_candidate, create_election, create_user


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
