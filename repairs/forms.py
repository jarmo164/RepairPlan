from django import forms

from .models import Repair, RepairComment


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = [
            'product_code',
            'quantity',
            'client_or_group',
            'department',
            'priority',
            'status',
            'assigned_to',
            'comment',
        ]


class RepairCommentForm(forms.ModelForm):
    class Meta:
        model = RepairComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
