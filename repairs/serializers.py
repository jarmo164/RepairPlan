from rest_framework import serializers

from .models import Department, Repair, RepairComment, RepairStatusLog, UserProfile


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'is_active']


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'department', 'phone', 'notes']


class RepairListSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()
    priority_label = serializers.CharField(source='get_priority_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Repair
        fields = [
            'id', 'product_code', 'quantity', 'client_or_group', 'department', 'created_at',
            'created_by', 'priority', 'priority_label', 'status', 'status_label', 'assigned_to', 'updated_at',
        ]


class RepairDetailSerializer(RepairListSerializer):
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta(RepairListSerializer.Meta):
        fields = RepairListSerializer.Meta.fields + ['comment', 'comments_count']


class RepairCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = RepairComment
        fields = ['id', 'author', 'comment', 'created_at']


class RepairStatusLogSerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()

    class Meta:
        model = RepairStatusLog
        fields = ['id', 'field_name', 'old_value', 'new_value', 'changed_by', 'created_at']
