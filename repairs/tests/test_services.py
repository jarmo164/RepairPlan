from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from repairs.models import Department, Repair
from repairs.permissions import ensure_role_groups
from repairs.services import change_status


class WorkflowServiceTests(TestCase):
    def setUp(self):
        ensure_role_groups()
        User = get_user_model()
        self.department = Department.objects.create(name='Ladu', code='LADU')
        self.master = User.objects.create_user(username='master', password='secret123')
        self.master.groups.add(self.master.groups.model.objects.get(name='repair_master'))
        self.repairer = User.objects.create_user(username='repairer', password='secret123')
        self.repairer.groups.add(self.repairer.groups.model.objects.get(name='repairer'))
        self.repair = Repair.objects.create(
            product_code='ABC-1', quantity=1, client_or_group='Client', department=self.department,
            created_by=self.master, assigned_to=self.repairer, status=Repair.Status.REVIEWED,
        )

    def test_repairer_can_move_reviewed_to_in_progress(self):
        change_status(repair=self.repair, status=Repair.Status.IN_PROGRESS, changed_by=self.repairer)
        self.repair.refresh_from_db()
        self.assertEqual(self.repair.status, Repair.Status.IN_PROGRESS)

    def test_repairer_cannot_return_item(self):
        with self.assertRaises(ValidationError):
            change_status(repair=self.repair, status=Repair.Status.RETURNED, changed_by=self.repairer)
