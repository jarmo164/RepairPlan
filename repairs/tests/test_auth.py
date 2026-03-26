from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='authuser', password='secret12345')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logi sisse')

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('repairs:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_login_redirects_to_dashboard(self):
        response = self.client.post(reverse('login'), {'username': 'authuser', 'password': 'secret12345'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('repairs:dashboard'))
