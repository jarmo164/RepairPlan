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
        fields = ['id', 'user', 'department', 'specialty', 'phone', 'notes']


class RepairListSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    assigned_to = serializers.StringRelatedField()
    priority_label = serializers.CharField(source='get_priority_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)
    repair_track_label = serializers.CharField(source='get_repair_track_display', read_only=True)
    assigned_to_specialty = serializers.SerializerMethodField()

    class Meta:
        model = Repair
        fields = [
            'id', 'product_code', 'quantity', 'client_or_group', 'department', 'repair_track', 'created_at',
            'created_by', 'priority', 'priority_label', 'status', 'status_label', 'assigned_to', 'assigned_to_specialty', 'repair_track_label', 'updated_at',
        ]



    def get_assigned_to_specialty(self, obj):
        if obj.assigned_to and hasattr(obj.assigned_to, 'profile'):
            return obj.assigned_to.profile.specialty
        return None

class RepairDetailSerializer(RepairListSerializer):
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta(RepairListSerializer.Meta):
        fields = RepairListSerializer.Meta.fields + ['comment', 'comments_count']


class RepairCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['product_code', 'quantity', 'client_or_group', 'department', 'repair_track', 'comment']


class RepairUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repair
        fields = ['product_code', 'quantity', 'client_or_group', 'department', 'repair_track', 'priority', 'status', 'assigned_to', 'comment']


class RepairAssignSerializer(serializers.Serializer):
    assigned_to = serializers.IntegerField(allow_null=True, required=False)


class RepairStatusChangeSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Repair.Status.choices)


class RepairPriorityChangeSerializer(serializers.Serializer):
    priority = serializers.ChoiceField(choices=Repair.Priority.choices)


class RepairCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RepairComment
        fields = ['id', 'author', 'comment', 'created_at']


class RepairerWorkloadSerializer(serializers.Serializer):
    username = serializers.CharField()
    total = serializers.IntegerField()


class RepairStatusLogSerializer(serializers.ModelSerializer):
    changed_by = serializers.StringRelatedField()
    field_label = serializers.SerializerMethodField()

    class Meta:
        model = RepairStatusLog
        fields = ['id', 'field_name', 'field_label', 'old_value', 'new_value', 'changed_by', 'created_at']

    def get_field_label(self, obj):
        mapping = {
            'repair_created': 'Parandus loodud',
            'status': 'Staatus',
            'priority': 'Prioriteet',
            'assigned_to': 'Parandaja',
        }
        return mapping.get(obj.field_name, obj.field_name)


class RepairCombinedActionSerializer(serializers.Serializer):
    assigned_to = serializers.IntegerField(allow_null=True, required=False)
    priority = serializers.ChoiceField(choices=Repair.Priority.choices, required=False)
    status = serializers.ChoiceField(choices=Repair.Status.choices, required=False)
    comment = serializers.CharField(required=False, allow_blank=True)
