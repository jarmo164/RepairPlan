from .models import Repair, RepairStatusLog

ALLOWED_STATUS_TRANSITIONS = {
    Repair.Status.NOT_STARTED: {Repair.Status.REVIEWED},
    Repair.Status.REVIEWED: {Repair.Status.IN_PROGRESS, Repair.Status.RETURNED},
    Repair.Status.IN_PROGRESS: {Repair.Status.ON_HOLD, Repair.Status.COMPLETED, Repair.Status.RETURNED},
    Repair.Status.ON_HOLD: {Repair.Status.IN_PROGRESS},
    Repair.Status.COMPLETED: set(),
    Repair.Status.RETURNED: set(),
}


def log_change(*, repair, changed_by, field_name, old_value, new_value):
    return RepairStatusLog.objects.create(
        repair=repair,
        changed_by=changed_by,
        field_name=field_name,
        old_value='' if old_value is None else str(old_value),
        new_value='' if new_value is None else str(new_value),
    )


def create_repair(*, created_by, **data):
    repair = Repair.objects.create(created_by=created_by, **data)
    log_change(repair=repair, changed_by=created_by, field_name='repair_created', old_value='', new_value=repair.status)
    return repair


def update_repair(*, repair, changed_by, **data):
    tracked_fields = {'priority', 'status', 'assigned_to'}
    for field, value in data.items():
        old_value = getattr(repair, field, None)
        setattr(repair, field, value)
        if field in tracked_fields and old_value != value:
            log_change(repair=repair, changed_by=changed_by, field_name=field, old_value=old_value, new_value=value)
    repair.save()
    return repair


def assign_repair(*, repair, assigned_to, changed_by):
    old_value = repair.assigned_to_id
    repair.assigned_to = assigned_to
    repair.save(update_fields=['assigned_to', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='assigned_to', old_value=old_value, new_value=assigned_to.pk if assigned_to else '')


def change_priority(*, repair, priority, changed_by):
    old_value = repair.priority
    repair.priority = priority
    repair.save(update_fields=['priority', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='priority', old_value=old_value, new_value=priority)


def change_status(*, repair, status, changed_by):
    current = repair.status
    allowed = ALLOWED_STATUS_TRANSITIONS.get(current, set())
    if status != current and status not in allowed:
        raise ValueError(f'Invalid status transition: {current} -> {status}')
    repair.status = status
    repair.save(update_fields=['status', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='status', old_value=current, new_value=status)
