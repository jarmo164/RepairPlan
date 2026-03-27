from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from repairs.models import Department, Repair, RepairStatusLog
from repairs.permissions import ensure_role_groups


class DashboardSelfClaimTests(TestCase):
    def setUp(self):
        ensure_role_groups()
        User = get_user_model()
        self.department = Department.objects.create(name='FCT', code='FCT')
        self.master = User.objects.create_user(username='master', password='secret123')
        self.master.groups.add(self.master.groups.model.objects.get(name='repair_master'))
        self.repairer = User.objects.create_user(username='repairer', password='secret123')
        self.repairer.groups.add(self.repairer.groups.model.objects.get(name='repairer'))
        self.repair = Repair.objects.create(
            product_code='SELF-1', quantity=1, client_or_group='Client', department=self.department,
            created_by=self.master, assigned_to=self.repairer
        )
        RepairStatusLog.objects.create(
            repair=self.repair,
            changed_by=self.repairer,
            field_name='assignment_source',
            old_value='',
            new_value='SELF_CLAIMED',
        )

    def test_dashboard_summary_contains_self_claimed_lists(self):
        self.client.login(username='master', password='secret123')
        response = self.client.get(reverse('repairs:api-dashboard-summary'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('self_claimed', data)
        self.assertIn('weekend_self_claimed', data)
