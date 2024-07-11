from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.tests.helpers import create_election


class ElectionApiTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.election1 = create_election()
    self.election2 = create_election()

  def test_list_elections(self):
    """Should return a list of elections"""
    response = self.client.get(reverse('election:election-list'))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 2)

  def test_retrieve_election(self):
    """Should retrieve the details of a specific election"""
    url = reverse('election:election-detail', args=[self.election1.slug])
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['title'], self.election1.title)

  def test_retrieve_nonexistent_election(self):
    """Should return a 404 if nonexisting slug"""
    url = reverse('election:election-detail', args=['non-existing'])
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)
