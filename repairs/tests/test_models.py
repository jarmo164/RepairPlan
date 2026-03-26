from django.contrib.auth import get_user_model
from django.test import TestCase

from repairs.models import Department


class UserProfileSignalTests(TestCase):
    def test_profile_created_with_user(self):
        user = get_user_model().objects.create_user(username='tester', password='secret123')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNone(user.profile.department)

    def test_department_str(self):
        department = Department.objects.create(name='Ladu', code='LADU')
        self.assertIn('Ladu', str(department))
