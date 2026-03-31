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

    def test_repairs_api_hides_returned_by_default(self):
        change_status(repair=self.repair, status=Repair.Status.RETURNED, changed_by=self.master)
        response = self.client.get(reverse('repairs:api-repairs'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pagination']['count'], 0)

    def test_repairs_api_can_filter_returned(self):
        change_status(repair=self.repair, status=Repair.Status.RETURNED, changed_by=self.master)
        response = self.client.get(reverse('repairs:api-repairs'), {'status': Repair.Status.RETURNED})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pagination']['count'], 1)

    def test_repairs_api_can_filter_by_track(self):
        self.repair.repair_track = Repair.Track.ELECTRONICS
        self.repair.save(update_fields=['repair_track'])
        response = self.client.get(reverse('repairs:api-repairs'), {'repair_track': Repair.Track.ELECTRONICS})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pagination']['count'], 1)

    def test_repairs_api_can_filter_unassigned(self):
        response = self.client.get(reverse('repairs:api-repairs'), {'unassigned_only': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pagination']['count'], 1)

    def test_bulk_update_status_and_priority(self):
        repair_two = Repair.objects.create(
            product_code='ABC-2', quantity=1, client_or_group='Client 2', department=self.department, created_by=self.master
        )
        response = self.client.post(
            reverse('repairs:api-repair-bulk-update'),
            data={
                'repair_ids': [self.repair.id, repair_two.id],
                'status': Repair.Status.IN_PROGRESS,
                'priority': Repair.Priority.HIGH,
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.repair.refresh_from_db()
        repair_two.refresh_from_db()
        self.assertEqual(self.repair.status, Repair.Status.IN_PROGRESS)
        self.assertEqual(repair_two.status, Repair.Status.IN_PROGRESS)
        self.assertEqual(self.repair.priority, Repair.Priority.HIGH)
        self.assertEqual(repair_two.priority, Repair.Priority.HIGH)

    def test_bulk_update_assigns_repairer(self):
        User = get_user_model()
        repairer = User.objects.create_user(username='bulk-repairer', password='secret123')
        repairer.groups.add(repairer.groups.model.objects.get(name='repairer'))
        response = self.client.post(
            reverse('repairs:api-repair-bulk-update'),
            data={
                'repair_ids': [self.repair.id],
                'assigned_to': repairer.id,
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.repair.refresh_from_db()
        self.assertEqual(self.repair.assigned_to_id, repairer.id)

    def test_export_returns_csv(self):
        response = self.client.get(reverse('repairs:api-repairs-export'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        reader = csv.reader(StringIO(content))
        rows = list(reader)
        self.assertEqual(rows[0][0], 'ID')
        self.assertEqual(rows[1][1], 'ABC-1')
