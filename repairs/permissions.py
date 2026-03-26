from django.contrib.auth.models import Group

ROLE_DEPARTMENT_MANAGER = 'department_manager'
ROLE_REPAIR_MASTER = 'repair_master'
ROLE_REPAIRER = 'repairer'
ROLE_ADMINISTRATOR = 'administrator'
ROLE_NAMES = [ROLE_DEPARTMENT_MANAGER, ROLE_REPAIR_MASTER, ROLE_REPAIRER, ROLE_ADMINISTRATOR]

ROLE_PERMISSION_MATRIX = {
    ROLE_DEPARTMENT_MANAGER: {
        'can_view_department_repairs': True,
        'can_create_repairs': True,
        'can_assign_repairs': False,
        'can_change_priority': False,
        'can_change_any_status': False,
    },
    ROLE_REPAIR_MASTER: {
        'can_view_all_repairs': True,
        'can_create_repairs': True,
        'can_assign_repairs': True,
        'can_change_priority': True,
        'can_change_any_status': True,
        'can_view_dashboard': True,
    },
    ROLE_REPAIRER: {
        'can_view_assigned_repairs_only': True,
        'can_create_repairs': False,
        'can_assign_repairs': False,
        'can_change_own_status': True,
    },
    ROLE_ADMINISTRATOR: {
        'can_manage_system': True,
        'can_view_all_repairs': True,
        'can_assign_repairs': True,
        'can_change_priority': True,
        'can_change_any_status': True,
        'can_view_dashboard': True,
    },
}

ROLE_PERMISSION_MATRIX = {
    ROLE_DEPARTMENT_MANAGER: {
        'can_view_department_repairs': True,
        'can_create_repairs': True,
        'can_assign_repairs': False,
        'can_change_priority': False,
        'can_change_any_status': False,
    },
    ROLE_REPAIR_MASTER: {
        'can_view_all_repairs': True,
        'can_create_repairs': True,
        'can_assign_repairs': True,
        'can_change_priority': True,
        'can_change_any_status': True,
        'can_view_dashboard': True,
    },
    ROLE_REPAIRER: {
        'can_view_assigned_repairs_only': True,
        'can_create_repairs': False,
        'can_assign_repairs': False,
        'can_change_own_status': True,
    },
    ROLE_ADMINISTRATOR: {
        'can_manage_system': True,
        'can_view_all_repairs': True,
        'can_assign_repairs': True,
        'can_change_priority': True,
        'can_change_any_status': True,
        'can_view_dashboard': True,
    },
}


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
