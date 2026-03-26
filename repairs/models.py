from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    phone = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f'Profile<{self.user.username}>'


class Repair(models.Model):
    class Priority(models.TextChoices):
        HIGH = 'HIGH', 'Kõrge'
        MEDIUM = 'MEDIUM', 'Keskmine'
        LOW = 'LOW', 'Madal'

    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Alustamata'
        REVIEWED = 'REVIEWED', 'Üle vaadatud'
        IN_PROGRESS = 'IN_PROGRESS', 'Töös'
        ON_HOLD = 'ON_HOLD', 'Ootel'
        COMPLETED = 'COMPLETED', 'Lõpetatud'
        RETURNED = 'RETURNED', 'Tagastatud'

    product_code = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    client_or_group = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='repairs')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_repairs')
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_repairs',
    )
    comment = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return f'#{self.pk} {self.product_code}'


class RepairComment(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='repair_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment<{self.repair_id}:{self.author_id}>'


class RepairStatusLog(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='status_logs')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='repair_status_logs')
    field_name = models.CharField(max_length=64)
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Log<{self.repair_id}:{self.field_name}>'
