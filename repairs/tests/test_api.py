import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from repairs.models import Department, Repair
from repairs.permissions import ensure_role_groups
from repairs.services import change_status


class RepairApiTests(TestCase):
    def setUp(self):
        ensure_role_groups()
        User = get_user_model()
        self.department = Department.objects.create(name='Ladu', code='LADU')
        self.master = User.objects.create_user(username='master', password='secret123')
        self.master.groups.add(self.master.groups.model.objects.get(name='repair_master'))
        self.client.login(username='master', password='secret123')
        self.repair = Repair.objects.create(
            product_code='ABC-1', quantity=2, client_or_group='Client', department=self.department, created_by=self.master
        )

    def test_repairs_api_returns_results(self):
        response = self.client.get(reverse('repairs:api-repairs'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pagination']['count'], 1)

    def test_dashboard_summary_endpoint(self):
        response = self.client.get(reverse('repairs:api-dashboard-summary'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('total', response.json())

    def test_export_returns_csv(self):
        response = self.client.get(reverse('repairs:api-repairs-export'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        reader = csv.reader(StringIO(content))
        rows = list(reader)
        self.assertEqual(rows[0][0], 'ID')
        self.assertEqual(rows[1][1], 'ABC-1')
