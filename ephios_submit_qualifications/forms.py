from django import forms
from .models import QualificationRequest

class QualificationSubmitForm(forms.ModelForm):
    class Meta:
        model = QualificationRequest
        fields = ['qualification', 'qualification_date']
        widgets = {
            'qualification': forms.Select(attrs={"placeholder": "Select Qualification"}),
            'qualification_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

class QualificationDetailForm(forms.ModelForm):
    user = forms.CharField(
        label="User",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    qualification = forms.CharField(
        label="Qualification",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    requested_at = forms.DateTimeField(
        required=False,
        label="Requested At",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': 'readonly'})
    )
    expires_at = forms.DateField(
        required=False,
        label="Expires At",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    reason = forms.CharField(
        required=False,
        label="Reason for Action",
        widget=forms.Textarea,
        help_text="Optional reason for the action taken on this request."
    )

    class Meta:
        model = QualificationRequest
        fields = ['qualification_date']
        widgets = {
            'qualification_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance and hasattr(instance, 'user') and instance.user_id:
            self.fields['user'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
            self.fields['user'].initial = instance.user.get_full_name()

        if instance and hasattr(instance, 'qualification') and instance.qualification_id:
            self.fields['qualification'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
            self.fields['qualification'].initial = str(instance.qualification)

        if instance and instance.requested_at:
            self.initial['requested_at'] = instance.requested_at.strftime('%Y-%m-%dT%H:%M')

