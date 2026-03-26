from django.core.exceptions import ValidationError

from .models import Repair, RepairStatusLog
from .permissions import can_assign_repairs, can_change_priority, can_change_status, can_create_repairs

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
    if not can_create_repairs(created_by):
        raise ValidationError('Sul puudub õigus parandusi luua.')
    repair = Repair.objects.create(created_by=created_by, **data)
    log_change(repair=repair, changed_by=created_by, field_name='repair_created', old_value='', new_value=repair.status)
    return repair


def update_repair(*, repair, changed_by, **data):
    tracked_fields = {'priority', 'status', 'assigned_to'}
    for field, value in data.items():
        if field == 'assigned_to' and not can_assign_repairs(changed_by):
            raise ValidationError('Sul puudub õigus parandajat määrata.')
        if field == 'priority' and not can_change_priority(changed_by):
            raise ValidationError('Sul puudub õigus prioriteeti muuta.')
        if field == 'status' and not can_change_status(changed_by, own_assigned_only=repair.assigned_to_id == changed_by.id):
            raise ValidationError('Sul puudub õigus staatust muuta.')

        old_value = getattr(repair, field, None)
        setattr(repair, field, value)
        if field in tracked_fields and old_value != value:
            log_change(repair=repair, changed_by=changed_by, field_name=field, old_value=old_value, new_value=value)
    repair.save()
    return repair


def assign_repair(*, repair, assigned_to, changed_by):
    if not can_assign_repairs(changed_by):
        raise ValidationError('Sul puudub õigus parandajat määrata.')
    old_value = repair.assigned_to_id
    repair.assigned_to = assigned_to
    repair.save(update_fields=['assigned_to', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='assigned_to', old_value=old_value, new_value=assigned_to.pk if assigned_to else '')


def change_priority(*, repair, priority, changed_by):
    if not can_change_priority(changed_by):
        raise ValidationError('Sul puudub õigus prioriteeti muuta.')
    old_value = repair.priority
    repair.priority = priority
    repair.save(update_fields=['priority', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='priority', old_value=old_value, new_value=priority)


def change_status(*, repair, status, changed_by):
    own_assigned = repair.assigned_to_id == changed_by.id
    if not can_change_status(changed_by, own_assigned_only=own_assigned):
        raise ValidationError('Sul puudub õigus staatust muuta.')

    current = repair.status
    allowed = ALLOWED_STATUS_TRANSITIONS.get(current, set())
    if status != current and status not in allowed:
        raise ValidationError(f'Lubamatu staatuse üleminek: {current} -> {status}')

    repair.status = status
    repair.save(update_fields=['status', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='status', old_value=current, new_value=status)
