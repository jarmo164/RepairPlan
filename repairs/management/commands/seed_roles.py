from django.core.management.base import BaseCommand

from repairs.permissions import ROLE_NAMES, ensure_role_groups


class Command(BaseCommand):
    help = 'Create the default RepairPlan role groups.'

    def handle(self, *args, **options):
        ensure_role_groups()
        self.stdout.write(self.style.SUCCESS(f'Ensured roles: {", ".join(ROLE_NAMES)}'))
