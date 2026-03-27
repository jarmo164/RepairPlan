from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from repairs.models import Department, Repair
from repairs.permissions import ensure_role_groups


class RepairShelfTests(TestCase):
    def setUp(self):
        ensure_role_groups()
        User = get_user_model()
        self.department = Department.objects.create(name='FCT', code='FCT')
        self.repairer = User.objects.create_user(username='repairer', password='secret123')
        self.repairer.groups.add(self.repairer.groups.model.objects.get(name='repairer'))
        self.master = User.objects.create_user(username='master', password='secret123')
        self.master.groups.add(self.master.groups.model.objects.get(name='repair_master'))
        self.available = Repair.objects.create(
            product_code='FREE-1', quantity=1, client_or_group='Client', department=self.department,
            created_by=self.master, status=Repair.Status.REVIEWED
        )

    def test_repair_shelf_page_renders(self):
        self.client.login(username='repairer', password='secret123')
        response = self.client.get(reverse('repairs:repair-shelf'))
        self.assertEqual(response.status_code, 200)

    def test_repairer_can_self_claim_work(self):
        self.client.login(username='repairer', password='secret123')
        response = self.client.post(
            reverse('repairs:api-repair-self-claim', args=[self.available.id]),
            content_type='application/json',
            data='{}',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        self.available.refresh_from_db()
        self.assertEqual(self.available.assigned_to, self.repairer)
