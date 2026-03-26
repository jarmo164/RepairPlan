from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from repairs.models import Department, Repair
from repairs.permissions import ensure_role_groups
from repairs.services import log_change


class Command(BaseCommand):
    help = 'Seed realistic demo data for RepairPlan.'

    def handle(self, *args, **options):
        ensure_role_groups()
        User = get_user_model()

        departments = {
            'FCT': Department.objects.get_or_create(code='FCT', defaults={'name': 'FCT'})[0],
            'SEL': Department.objects.get_or_create(code='SEL', defaults={'name': 'SEL'})[0],
            'ICT': Department.objects.get_or_create(code='ICT', defaults={'name': 'ICT'})[0],
            'THT': Department.objects.get_or_create(code='THT', defaults={'name': 'THT'})[0],
        }

        admin_user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.email = admin_user.email or 'admin@example.com'
        admin_user.set_password('admin12345')
        admin_user.save()

        master, _ = User.objects.get_or_create(username='mart', defaults={'first_name': 'Mart', 'email': 'mart@example.com'})
        master.set_password('demo12345')
        master.save()
        master.groups.add(master.groups.model.objects.get(name='repair_master'))
        master.profile.department = departments['FCT']
        master.profile.save()

        kati, _ = User.objects.get_or_create(username='kati', defaults={'first_name': 'Kati', 'email': 'kati@example.com'})
        kati.set_password('demo12345')
        kati.save()
        kati.groups.add(kati.groups.model.objects.get(name='repairer'))
        kati.profile.department = departments['ICT']
        kati.profile.save()

        manager_fct, _ = User.objects.get_or_create(username='juht_fct', defaults={'first_name': 'FCT', 'last_name': 'Juht', 'email': 'fct@example.com'})
        manager_fct.set_password('demo12345')
        manager_fct.save()
        manager_fct.groups.add(manager_fct.groups.model.objects.get(name='department_manager'))
        manager_fct.profile.department = departments['FCT']
        manager_fct.profile.save()

        manager_sel, _ = User.objects.get_or_create(username='juht_sel', defaults={'first_name': 'SEL', 'last_name': 'Juht', 'email': 'sel@example.com'})
        manager_sel.set_password('demo12345')
        manager_sel.save()
        manager_sel.groups.add(manager_sel.groups.model.objects.get(name='department_manager'))
        manager_sel.profile.department = departments['SEL']
        manager_sel.profile.save()

        demo_repairs = [
            {
                'product_code': '67482', 'quantity': 5, 'client_or_group': 'Schneider1', 'department': departments['FCT'],
                'priority': Repair.Priority.HIGH, 'status': Repair.Status.IN_PROGRESS, 'assigned_to': master,
                'comment': 'Alustatud', 'created_by': manager_fct,
            },
            {
                'product_code': '67609', 'quantity': 1, 'client_or_group': 'Schneider1', 'department': departments['FCT'],
                'priority': Repair.Priority.MEDIUM, 'status': Repair.Status.NOT_STARTED, 'assigned_to': None,
                'comment': 'Ootab ülevaatust', 'created_by': manager_fct,
            },
            {
                'product_code': '56191', 'quantity': 4, 'client_or_group': 'ABB ICT/THT', 'department': departments['SEL'],
                'priority': Repair.Priority.LOW, 'status': Repair.Status.NOT_STARTED, 'assigned_to': None,
                'comment': '', 'created_by': manager_sel,
            },
            {
                'product_code': '67922', 'quantity': 6, 'client_or_group': 'Schneider ICT', 'department': departments['ICT'],
                'priority': Repair.Priority.HIGH, 'status': Repair.Status.NOT_STARTED, 'assigned_to': kati,
                'comment': 'Kiire töö', 'created_by': manager_fct,
            },
            {
                'product_code': '41985', 'quantity': 1, 'client_or_group': 'Kone', 'department': departments['THT'],
                'priority': Repair.Priority.MEDIUM, 'status': Repair.Status.NOT_STARTED, 'assigned_to': None,
                'comment': '', 'created_by': manager_sel,
            },
        ]

        created = 0
        for item in demo_repairs:
            repair, was_created = Repair.objects.get_or_create(
                product_code=item['product_code'],
                defaults=item,
            )
            if was_created:
                created += 1
                log_change(repair=repair, changed_by=item['created_by'], field_name='repair_created', old_value='', new_value=repair.status)
                if repair.assigned_to:
                    log_change(repair=repair, changed_by=item['created_by'], field_name='assigned_to', old_value='', new_value=repair.assigned_to.username)
                if repair.status != Repair.Status.NOT_STARTED:
                    log_change(repair=repair, changed_by=item['created_by'], field_name='status', old_value=Repair.Status.NOT_STARTED, new_value=repair.status)
                if repair.priority != Repair.Priority.MEDIUM:
                    log_change(repair=repair, changed_by=item['created_by'], field_name='priority', old_value=Repair.Priority.MEDIUM, new_value=repair.priority)

        self.stdout.write(self.style.SUCCESS(f'Seeded {created} demo repairs.'))
        self.stdout.write('Demo users: admin/admin12345, mart/demo12345, kati/demo12345, juht_fct/demo12345, juht_sel/demo12345')
