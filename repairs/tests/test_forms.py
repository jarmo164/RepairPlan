from django.test import TestCase

from repairs.forms import RepairCreateForm
from repairs.models import Department


class RepairFormTests(TestCase):
    def test_repair_create_form_valid(self):
        department = Department.objects.create(name='Ladu', code='LADU')
        form = RepairCreateForm(data={
            'product_code': 'ABC-1',
            'quantity': 3,
            'client_or_group': 'Testgrupp',
            'department': department.id,
            'comment': 'Algne märkus',
        })
        self.assertTrue(form.is_valid())
