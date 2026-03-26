from django.contrib.auth.models import Group

ROLE_DEPARTMENT_MANAGER = 'department_manager'
ROLE_REPAIR_MASTER = 'repair_master'
ROLE_REPAIRER = 'repairer'
ROLE_ADMINISTRATOR = 'administrator'
ROLE_NAMES = [ROLE_DEPARTMENT_MANAGER, ROLE_REPAIR_MASTER, ROLE_REPAIRER, ROLE_ADMINISTRATOR]


def ensure_role_groups():
    for name in ROLE_NAMES:
        Group.objects.get_or_create(name=name)


def user_in_role(user, role_name: str) -> bool:
    return bool(user and user.is_authenticated and user.groups.filter(name=role_name).exists())


def is_department_manager(user) -> bool:
    return user_in_role(user, ROLE_DEPARTMENT_MANAGER)


def is_repair_master(user) -> bool:
    return user_in_role(user, ROLE_REPAIR_MASTER)


def is_repairer(user) -> bool:
    return user_in_role(user, ROLE_REPAIRER)


def is_administrator(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_superuser or user_in_role(user, ROLE_ADMINISTRATOR)))
