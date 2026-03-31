from django.db.models import Count

from .models import Repair
from .permissions import is_administrator, is_department_manager, is_repair_master, is_repairer


def hide_returned_by_default(queryset, params=None):
    params = params or {}
    include_returned = str(params.get('include_returned') or '').lower() in {'1', 'true', 'yes', 'on'}
    explicit_status = params.get('status')
    if explicit_status or include_returned:
        return queryset
    return queryset.exclude(status=Repair.Status.RETURNED)


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


def filter_repairs_for_user(user, params=None):
    params = params or {}
    qs = hide_returned_by_default(repairs_visible_to(user), params)

    search = (params.get('search') or '').strip()
    if search:
        qs = qs.filter(product_code__icontains=search)

    department = params.get('department')
    if department:
        qs = qs.filter(department_id=department)

    client_or_group = (params.get('client_or_group') or '').strip()
    if client_or_group:
        qs = qs.filter(client_or_group__icontains=client_or_group)

    status = params.get('status')
    if status:
        qs = qs.filter(status=status)

    priority = params.get('priority')
    if priority:
        qs = qs.filter(priority=priority)

    assigned_to = params.get('assigned_to')
    if assigned_to:
        qs = qs.filter(assigned_to_id=assigned_to)

    ordering = params.get('ordering') or '-created_at'
    allowed_ordering = {'created_at', '-created_at', 'priority', '-priority', 'status', '-status'}
    if ordering in allowed_ordering:
        qs = qs.order_by(ordering)

    return qs


def my_work_for(user):
    return repairs_visible_to(user).exclude(status=Repair.Status.RETURNED).filter(assigned_to=user)


def dashboard_summary_for(user):
    qs = repairs_visible_to(user).exclude(status=Repair.Status.RETURNED)
    return {
        'total': qs.count(),
        'not_started': qs.filter(status=Repair.Status.NOT_STARTED).count(),
        'in_progress': qs.filter(status=Repair.Status.IN_PROGRESS).count(),
        'completed': qs.filter(status=Repair.Status.COMPLETED).count(),
        'high_priority': qs.filter(priority=Repair.Priority.HIGH).count(),
        'unassigned': qs.filter(assigned_to__isnull=True).count(),
    }


def dashboard_oldest_open_repairs_for(user, limit=5):
    return repairs_visible_to(user).exclude(status__in=[Repair.Status.COMPLETED, Repair.Status.RETURNED]).order_by('created_at')[:limit]


def dashboard_high_priority_open_repairs_for(user, limit=5):
    return (
        repairs_visible_to(user)
        .filter(priority=Repair.Priority.HIGH)
        .exclude(status__in=[Repair.Status.COMPLETED, Repair.Status.RETURNED])
        .order_by('created_at')[:limit]
    )


def dashboard_unassigned_repairs_for(user, limit=5):
    return (
        repairs_visible_to(user)
        .filter(assigned_to__isnull=True)
        .exclude(status__in=[Repair.Status.COMPLETED, Repair.Status.RETURNED])
        .order_by('created_at')[:limit]
    )


def dashboard_repair_counts_by_repairer(user):
    visible_qs = repairs_visible_to(user)
    grouped = (
        visible_qs.exclude(assigned_to__isnull=True)
        .values('assigned_to_id', 'assigned_to__username')
        .annotate(total=Count('id'))
        .order_by('-total', 'assigned_to__username')
    )
    return [
        {
            'user_id': row['assigned_to_id'],
            'username': row['assigned_to__username'],
            'total': row['total'],
        }
        for row in grouped
    ]


def repair_list_summary_for(user):
    qs = repairs_visible_to(user).exclude(status=Repair.Status.RETURNED)
    return {
        'total': qs.count(),
        'high_priority': qs.filter(priority=Repair.Priority.HIGH).count(),
        'unassigned': qs.filter(assigned_to__isnull=True).count(),
        'in_progress': qs.filter(status=Repair.Status.IN_PROGRESS).count(),
    }


def repair_shelf_for(user):
    qs = Repair.objects.select_related('department', 'created_by', 'assigned_to').filter(assigned_to__isnull=True)
    qs = qs.exclude(status__in=[Repair.Status.COMPLETED, Repair.Status.RETURNED])

    if not user or not user.is_authenticated:
        return qs.none()
    if is_department_manager(user):
        department = getattr(getattr(user, 'profile', None), 'department', None)
        qs = qs.filter(department=department) if department else qs.none()
    elif is_repairer(user) and hasattr(user, 'profile') and user.profile.specialty == 'ELECTRONICS':
        qs = qs.filter(repair_track=Repair.Track.ELECTRONICS)

    return qs.order_by('priority', 'created_at')


def dashboard_self_claimed_repairs_for(user, limit=10):
    return (
        repairs_visible_to(user)
        .exclude(status=Repair.Status.RETURNED)
        .filter(status_logs__field_name='assignment_source', status_logs__new_value='SELF_CLAIMED')
        .distinct()
        .order_by('-updated_at')[:limit]
    )


def dashboard_weekend_self_claimed_repairs_for(user, limit=10):
    return (
        repairs_visible_to(user)
        .exclude(status=Repair.Status.RETURNED)
        .filter(
            status_logs__field_name='assignment_source',
            status_logs__new_value='SELF_CLAIMED',
            status_logs__created_at__week_day__in=[1, 7],
        )
        .distinct()
        .order_by('-updated_at')[:limit]
    )
