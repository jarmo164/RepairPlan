from django import forms

from .models import Repair, RepairComment

BASE_INPUT_CLASS = 'form-control'
BASE_SELECT_CLASS = 'form-select'


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.Textarea):
                css = BASE_INPUT_CLASS
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css = BASE_SELECT_CLASS
            else:
                css = BASE_INPUT_CLASS
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing} {css}'.strip()


class RepairCreateForm(StyledModelForm):
    class Meta:
        model = Repair
        fields = [
            'product_code',
            'quantity',
            'client_or_group',
            'department',
            'repair_track',
            'priority',
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class RepairUpdateForm(StyledModelForm):
    class Meta:
        model = Repair
        fields = [
            'product_code',
            'quantity',
            'client_or_group',
            'department',
            'repair_track',
            'priority',
            'status',
            'assigned_to',
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


class RepairCommentForm(StyledModelForm):
    class Meta:
        model = RepairComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Lisa kommentaar…'}),
        }
