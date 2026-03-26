from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings

from repairs.models import Department, Repair
from repairs.notifications import send_assignment_notification, send_status_change_notification


@override_settings(
    REPAIRPLAN_NOTIFICATIONS_ENABLED=True,
    DEFAULT_FROM_EMAIL='noreply@example.com',
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
)
class NotificationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.department = Department.objects.create(name='Ladu', code='LADU')
        self.creator = User.objects.create_user(username='creator', password='secret123', email='creator@example.com')
        self.assignee = User.objects.create_user(username='assignee', password='secret123', email='assignee@example.com')
        self.repair = Repair.objects.create(
            product_code='ABC-1', quantity=1, client_or_group='Client', department=self.department,
            created_by=self.creator, assigned_to=self.assignee,
        )

    def test_assignment_notification_sends_email(self):
        sent = send_assignment_notification(repair=self.repair, assigned_to=self.assignee, changed_by=self.creator)
        self.assertTrue(sent)
        self.assertEqual(len(mail.outbox), 1)

    def test_status_change_notification_sends_email(self):
        self.repair.status = Repair.Status.IN_PROGRESS
        sent = send_status_change_notification(repair=self.repair, changed_by=self.creator)
        self.assertTrue(sent)
        self.assertEqual(len(mail.outbox), 1)
