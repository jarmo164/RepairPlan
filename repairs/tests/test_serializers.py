from django.contrib.auth import get_user_model
from django.test import TestCase

from repairs.models import Department, Repair, RepairComment, RepairStatusLog
from repairs.serializers import (
    RepairCommentSerializer,
    RepairCreateSerializer,
    RepairStatusLogSerializer,
    RepairUpdateSerializer,
)


class RepairSerializerTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Ladu', code='LADU')
        self.user = get_user_model().objects.create_user(username='tester', password='secret123')
        self.repair = Repair.objects.create(
            product_code='ABC-1',
            quantity=2,
            client_or_group='Client',
            department=self.department,
            created_by=self.user,
        )

    def test_repair_create_serializer_valid(self):
        serializer = RepairCreateSerializer(data={
            'product_code': 'XYZ-2',
            'quantity': 5,
            'client_or_group': 'Group',
            'department': self.department.id,
            'comment': 'Test',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_repair_update_serializer_allows_partial_fields(self):
        serializer = RepairUpdateSerializer(data={'priority': Repair.Priority.HIGH}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_comment_serializer_output(self):
        comment = RepairComment.objects.create(repair=self.repair, author=self.user, comment='Tere')
        data = RepairCommentSerializer(comment).data
        self.assertEqual(data['comment'], 'Tere')
        self.assertEqual(data['author'], 'tester')

    def test_status_log_serializer_has_field_label(self):
        log = RepairStatusLog.objects.create(
            repair=self.repair,
            changed_by=self.user,
            field_name='status',
            old_value='NOT_STARTED',
            new_value='IN_PROGRESS',
        )
        data = RepairStatusLogSerializer(log).data
        self.assertEqual(data['field_label'], 'Staatus')
