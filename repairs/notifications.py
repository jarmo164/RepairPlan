from django.conf import settings
from django.core.mail import send_mail


def notifications_enabled() -> bool:
    return bool(getattr(settings, 'REPAIRPLAN_NOTIFICATIONS_ENABLED', False) and getattr(settings, 'DEFAULT_FROM_EMAIL', ''))


def send_assignment_notification(*, repair, assigned_to, changed_by):
    if not notifications_enabled() or not assigned_to or not assigned_to.email:
        return False
    send_mail(
        subject=f'RepairPlan: sulle määrati töö #{repair.id}',
        message=(
            f'Tere {assigned_to.get_username()},\n\n'
            f'Sulle määrati parandustöö #{repair.id} ({repair.product_code}).\n'
            f'Muutja: {changed_by.get_username()}\n'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[assigned_to.email],
        fail_silently=True,
    )
    return True


def send_status_change_notification(*, repair, changed_by):
    recipients = []
    if repair.created_by.email:
        recipients.append(repair.created_by.email)
    if repair.assigned_to and repair.assigned_to.email and repair.assigned_to.email not in recipients:
        recipients.append(repair.assigned_to.email)
    if not notifications_enabled() or not recipients:
        return False
    send_mail(
        subject=f'RepairPlan: töö #{repair.id} staatus muutus',
        message=(
            f'Töö #{repair.id} ({repair.product_code}) staatus on nüüd {repair.get_status_display()}.\n'
            f'Muutja: {changed_by.get_username()}\n'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=True,
    )
    return True
