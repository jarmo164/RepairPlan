from django.core.exceptions import ValidationError

from .models import Repair, RepairComment, RepairStatusLog
from .notifications import send_assignment_notification, send_status_change_notification
from .permissions import can_assign_repairs, can_change_priority, can_change_status, can_comment_on_repair, can_create_repairs, is_repair_master

ALLOWED_STATUS_TRANSITIONS = {
    Repair.Status.NOT_STARTED: {Repair.Status.REVIEWED},
    Repair.Status.REVIEWED: {Repair.Status.ELECTRONICS_REPAIR, Repair.Status.IN_PROGRESS, Repair.Status.RETURNED},
    Repair.Status.ELECTRONICS_REPAIR: {Repair.Status.IN_PROGRESS, Repair.Status.ON_HOLD, Repair.Status.COMPLETED, Repair.Status.RETURNED},
    Repair.Status.IN_PROGRESS: {Repair.Status.ELECTRONICS_REPAIR, Repair.Status.ON_HOLD, Repair.Status.COMPLETED, Repair.Status.RETURNED},
    Repair.Status.ON_HOLD: {Repair.Status.ELECTRONICS_REPAIR, Repair.Status.IN_PROGRESS},
    Repair.Status.COMPLETED: set(),
    Repair.Status.RETURNED: set(),
}

REPAIRER_ALLOWED_STATUS_TRANSITIONS = {
    Repair.Status.REVIEWED: {Repair.Status.ELECTRONICS_REPAIR, Repair.Status.IN_PROGRESS},
    Repair.Status.ELECTRONICS_REPAIR: {Repair.Status.IN_PROGRESS, Repair.Status.ON_HOLD, Repair.Status.COMPLETED},
    Repair.Status.IN_PROGRESS: {Repair.Status.ELECTRONICS_REPAIR, Repair.Status.ON_HOLD, Repair.Status.COMPLETED},
    Repair.Status.ON_HOLD: {Repair.Status.ELECTRONICS_REPAIR, Repair.Status.IN_PROGRESS},
}


def log_change(*, repair, changed_by, field_name, old_value, new_value):
    return RepairStatusLog.objects.create(
        repair=repair,
        changed_by=changed_by,
        field_name=field_name,
        old_value='' if old_value is None else str(old_value),
        new_value='' if new_value is None else str(new_value),
    )


def validate_status_transition(*, repair, status, changed_by):
    current = repair.status
    own_assigned = repair.assigned_to_id == changed_by.id

    if not can_change_status(changed_by, own_assigned_only=own_assigned):
        raise ValidationError('Sul puudub õigus staatust muuta.')

    if status == current:
        return

    if is_repair_master(changed_by) or changed_by.is_superuser:
        allowed = ALLOWED_STATUS_TRANSITIONS.get(current, set())
    elif own_assigned:
        allowed = REPAIRER_ALLOWED_STATUS_TRANSITIONS.get(current, set())
    else:
        allowed = set()

    if status not in allowed:
        raise ValidationError(
            f'Lubamatu staatuse üleminek: {current} -> {status}. '
            f'Lubatud: {", ".join(sorted(allowed)) or "puuduvad"}.'
        )


def create_repair(*, created_by, **data):
    if not can_create_repairs(created_by):
        raise ValidationError('Sul puudub õigus parandusi luua.')
    repair = Repair.objects.create(created_by=created_by, **data)
    log_change(repair=repair, changed_by=created_by, field_name='repair_created', old_value='', new_value=repair.status)
    return repair


def update_repair(*, repair, changed_by, **data):
    tracked_fields = {'priority', 'status', 'assigned_to'}
    if 'status' in data:
        validate_status_transition(repair=repair, status=data['status'], changed_by=changed_by)

    changed_fields = []
    for field, value in data.items():
        if field == 'assigned_to' and not can_assign_repairs(changed_by):
            raise ValidationError('Sul puudub õigus parandajat määrata.')
        if field == 'priority' and not can_change_priority(changed_by):
            raise ValidationError('Sul puudub õigus prioriteeti muuta.')

        old_value = getattr(repair, field, None)
        if old_value != value:
            setattr(repair, field, value)
            changed_fields.append(field)
            if field in tracked_fields:
                log_change(repair=repair, changed_by=changed_by, field_name=field, old_value=old_value, new_value=value)
    if changed_fields:
        repair.save()
    return repair


def assign_repair(*, repair, assigned_to, changed_by):
    if not can_assign_repairs(changed_by):
        raise ValidationError('Sul puudub õigus parandajat määrata.')
    old_value = repair.assigned_to_id
    new_value = assigned_to.pk if assigned_to else None
    if old_value == new_value:
        return None
    repair.assigned_to = assigned_to
    repair.save(update_fields=['assigned_to', 'updated_at'])
    log = log_change(repair=repair, changed_by=changed_by, field_name='assigned_to', old_value=old_value, new_value=assigned_to.pk if assigned_to else '')
    send_assignment_notification(repair=repair, assigned_to=assigned_to, changed_by=changed_by)
    return log


def change_priority(*, repair, priority, changed_by):
    if not can_change_priority(changed_by):
        raise ValidationError('Sul puudub õigus prioriteeti muuta.')
    old_value = repair.priority
    if old_value == priority:
        return None
    repair.priority = priority
    repair.save(update_fields=['priority', 'updated_at'])
    return log_change(repair=repair, changed_by=changed_by, field_name='priority', old_value=old_value, new_value=priority)


def change_status(*, repair, status, changed_by):
    validate_status_transition(repair=repair, status=status, changed_by=changed_by)
    current = repair.status
    if current == status:
        return None
    repair.status = status
    repair.save(update_fields=['status', 'updated_at'])
    log = log_change(repair=repair, changed_by=changed_by, field_name='status', old_value=current, new_value=status)
    send_status_change_notification(repair=repair, changed_by=changed_by)
    return log


def add_comment(*, repair, author, comment):
    if not can_comment_on_repair(author, repair):
        raise ValidationError('Sul puudub õigus sellele tööle kommentaari lisada.')
    cleaned = (comment or '').strip()
    if not cleaned:
        raise ValidationError('Kommentaar ei tohi olla tühi.')
    return RepairComment.objects.create(repair=repair, author=author, comment=cleaned)


def self_claim_repair(*, repair, claimed_by):
    if not claimed_by or not claimed_by.is_authenticated:
        raise ValidationError('Autentimine puudub.')
    if repair.assigned_to_id:
        raise ValidationError('See töö on juba kellelegi määratud.')
    repair.assigned_to = claimed_by
    repair.save(update_fields=['assigned_to', 'updated_at'])
    log_change(repair=repair, changed_by=claimed_by, field_name='assigned_to', old_value='', new_value=claimed_by.pk)
    log_change(repair=repair, changed_by=claimed_by, field_name='assignment_source', old_value='', new_value='SELF_CLAIMED')
    send_assignment_notification(repair=repair, assigned_to=claimed_by, changed_by=claimed_by)
    return repair
