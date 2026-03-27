from django.contrib import admin

from .models import Department, Repair, RepairComment, RepairStatusLog, UserProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'specialty', 'updated_at')
    list_select_related = ('user', 'department')
    list_filter = ('department', 'specialty')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'department__name')


class RepairCommentInline(admin.TabularInline):
    model = RepairComment
    extra = 0


class RepairStatusLogInline(admin.TabularInline):
    model = RepairStatusLog
    extra = 0
    readonly_fields = ('field_name', 'old_value', 'new_value', 'changed_by', 'created_at')
    can_delete = False


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_code', 'department', 'repair_track', 'priority', 'status', 'assigned_to', 'created_at')
    list_filter = ('repair_track', 'status', 'priority', 'department', 'assigned_to')
    search_fields = ('product_code', 'client_or_group', 'comment')
    list_select_related = ('department', 'created_by', 'assigned_to')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RepairCommentInline, RepairStatusLogInline]


@admin.register(RepairComment)
class RepairCommentAdmin(admin.ModelAdmin):
    list_display = ('repair', 'author', 'created_at')
    list_select_related = ('repair', 'author')
    search_fields = ('repair__product_code', 'author__username', 'comment')


@admin.register(RepairStatusLog)
class RepairStatusLogAdmin(admin.ModelAdmin):
    list_display = ('repair', 'field_name', 'old_value', 'new_value', 'changed_by', 'created_at')
    list_filter = ('field_name', 'created_at')
    list_select_related = ('repair', 'changed_by')
    search_fields = ('repair__product_code', 'field_name', 'old_value', 'new_value', 'changed_by__username')
