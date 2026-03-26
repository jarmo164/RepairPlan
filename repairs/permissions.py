from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission

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


def can_view_dashboard(user) -> bool:
    return is_administrator(user) or is_repair_master(user)


def can_create_repairs(user) -> bool:
    return is_administrator(user) or is_repair_master(user) or is_department_manager(user)


def can_assign_repairs(user) -> bool:
    return is_administrator(user) or is_repair_master(user)


def can_change_priority(user) -> bool:
    return is_administrator(user) or is_repair_master(user)


def can_change_status(user, *, own_assigned_only: bool = False) -> bool:
    if is_administrator(user) or is_repair_master(user):
        return True
    if own_assigned_only and is_repairer(user):
        return True
    return False


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        if is_administrator(user):
            return True
        return any(user_in_role(user, role) for role in self.allowed_roles)


class DashboardAccessMixin(RoleRequiredMixin):
    allowed_roles = [ROLE_REPAIR_MASTER, ROLE_ADMINISTRATOR]


class RepairApiPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
