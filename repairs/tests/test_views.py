from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from repairs.models import Department, Repair
from repairs.permissions import ensure_role_groups


class RepairHtmlViewTests(TestCase):
    def setUp(self):
        ensure_role_groups()
        User = get_user_model()
        self.department = Department.objects.create(name='FCT', code='FCT')

        self.manager = User.objects.create_user(username='manager', password='secret123')
        self.manager.groups.add(self.manager.groups.model.objects.get(name='department_manager'))
        self.manager.profile.department = self.department
        self.manager.profile.save()

        self.master = User.objects.create_user(username='master', password='secret123')
        self.master.groups.add(self.master.groups.model.objects.get(name='repair_master'))

        self.repairer = User.objects.create_user(username='repairer', password='secret123')
        self.repairer.groups.add(self.repairer.groups.model.objects.get(name='repairer'))

        self.repair = Repair.objects.create(
            product_code='ABC-1',
            quantity=1,
            client_or_group='Client',
            department=self.department,
            created_by=self.manager,
            assigned_to=self.repairer,
            status=Repair.Status.REVIEWED,
        )

    def test_repair_list_view_renders_for_manager(self):
        self.client.login(username='manager', password='secret123')
        response = self.client.get(reverse('repairs:repair-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repairs/repair_list.html')

    def test_repair_create_view_renders_for_manager(self):
        self.client.login(username='manager', password='secret123')
        response = self.client.get(reverse('repairs:repair-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repairs/repair_form.html')

    def test_repair_detail_view_renders_for_visible_repair(self):
        self.client.login(username='manager', password='secret123')
        response = self.client.get(reverse('repairs:repair-detail', args=[self.repair.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repairs/repair_detail.html')

    def test_repair_update_view_renders_for_master(self):
        self.client.login(username='master', password='secret123')
        response = self.client.get(reverse('repairs:repair-update', args=[self.repair.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repairs/repair_form.html')

    def test_my_work_view_renders_for_repairer(self):
        self.client.login(username='repairer', password='secret123')
        response = self.client.get(reverse('repairs:my-work'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repairs/my_work.html')

    def test_dashboard_view_renders_for_master(self):
        self.client.login(username='master', password='secret123')
        response = self.client.get(reverse('repairs:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repairs/dashboard.html')

    def test_department_manager_create_form_locks_department(self):
        self.client.login(username='manager', password='secret123')
        response = self.client.get(reverse('repairs:repair-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="%s"' % self.department.id)

    def test_department_manager_can_create_visible_repair(self):
        self.client.login(username='manager', password='secret123')
        response = self.client.post(reverse('repairs:repair-create'), {
            'product_code': 'NEW-1',
            'quantity': 2,
            'client_or_group': 'New Client',
            'department': self.department.id,
            'repair_track': 'GENERAL',
            'priority': 'HIGH',
            'comment': 'uus',
        })
        self.assertEqual(response.status_code, 302)
        created = Repair.objects.get(product_code='NEW-1')
        self.assertEqual(created.department, self.department)
        follow = self.client.get(reverse('repairs:repair-detail', args=[created.id]))
        self.assertEqual(follow.status_code, 200)
