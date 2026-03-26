from django.contrib.auth import get_user_model
from django.test import TestCase

from repairs.models import Department, Repair
from repairs.permissions import ensure_role_groups
from repairs.selectors import repairs_visible_to


class PermissionSelectorTests(TestCase):
    def setUp(self):
        ensure_role_groups()
        User = get_user_model()
        self.department_a = Department.objects.create(name='A-osakond', code='A')
        self.department_b = Department.objects.create(name='B-osakond', code='B')

        self.manager = User.objects.create_user(username='manager', password='secret123')
        self.manager.groups.add(self.manager.groups.model.objects.get(name='department_manager'))
        self.manager.profile.department = self.department_a
        self.manager.profile.save()

        self.master = User.objects.create_user(username='master', password='secret123')
        self.master.groups.add(self.master.groups.model.objects.get(name='repair_master'))

        self.repairer = User.objects.create_user(username='repairer', password='secret123')
        self.repairer.groups.add(self.repairer.groups.model.objects.get(name='repairer'))

        self.other = User.objects.create_user(username='other', password='secret123')

        self.repair_a = Repair.objects.create(
            product_code='A-1', quantity=1, client_or_group='Client A', department=self.department_a,
            created_by=self.manager, assigned_to=self.repairer,
        )
        self.repair_b = Repair.objects.create(
            product_code='B-1', quantity=1, client_or_group='Client B', department=self.department_b,
            created_by=self.master,
        )

    def test_department_manager_sees_only_own_department(self):
        qs = repairs_visible_to(self.manager)
        self.assertQuerySetEqual(qs.order_by('id'), [self.repair_a], transform=lambda x: x)

    def test_repair_master_sees_all(self):
        qs = repairs_visible_to(self.master)
        self.assertEqual(qs.count(), 2)

    def test_repairer_sees_only_assigned(self):
        qs = repairs_visible_to(self.repairer)
        self.assertQuerySetEqual(qs.order_by('id'), [self.repair_a], transform=lambda x: x)
