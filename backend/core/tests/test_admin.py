from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
  def setUp(self):
    """Create user and client"""
    self.client = Client()
    self.admin_user = get_user_model().objects.create_superuser(
      'admin',
      'admin@example.com',
    )
    self.client.force_login(self.admin_user)
    self.user = get_user_model().objects.create_user(
      username='user',
      email='user@example.com',
      name='User Tester'
    )

  def test_user_lists(self):
    """All fields should be included in the page"""
    url = reverse('admin:core_user_changelist')
    res = self.client.get(url)

    self.assertContains(res, self.user.username)
    self.assertContains(res, self.user.name)
    self.assertContains(res, self.user.email)

  def test_edit_user_page(self):
    """Should be able to access edit user page"""
    url = reverse('admin:core_user_change', args=[self.user.id])
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)

  def test_create_user_page(self):
    """Should be able to access create user page"""
    url = reverse('admin:core_user_add')
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)
