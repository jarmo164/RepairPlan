from .models import Repair
from .permissions import is_administrator, is_department_manager, is_repair_master, is_repairer


def repairs_visible_to(user):
    qs = Repair.objects.select_related('department', 'created_by', 'assigned_to')
    if not user or not user.is_authenticated:
        return qs.none()
    if is_administrator(user) or is_repair_master(user):
        return qs
    if is_repairer(user):
        return qs.filter(assigned_to=user)
    if is_department_manager(user):
        department = getattr(getattr(user, 'profile', None), 'department', None)
        return qs.filter(department=department) if department else qs.none()
    return qs.none()


def my_work_for(user):
    return repairs_visible_to(user).filter(assigned_to=user)


def dashboard_summary_for(user):
    qs = repairs_visible_to(user)
    return {
        'total': qs.count(),
        'not_started': qs.filter(status=Repair.Status.NOT_STARTED).count(),
        'in_progress': qs.filter(status=Repair.Status.IN_PROGRESS).count(),
        'completed': qs.filter(status=Repair.Status.COMPLETED).count(),
        'high_priority': qs.filter(priority=Repair.Priority.HIGH).count(),
    }
