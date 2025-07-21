from django.utils.translation import gettext_lazy as _
from django import forms
from .models import QualificationRequest

class QualificationSubmitForm(forms.ModelForm):
    image = forms.ImageField(
        required=True,
        label=_("Upload Image"),
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = QualificationRequest
        fields = ['qualification', 'qualification_date']
        widgets = {
            'qualification': forms.Select(attrs={"placeholder": _("Select Qualification")}),
            'qualification_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

class QualificationDetailForm(forms.Form):
    user = forms.CharField(
        label=_("User"),
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    qualification = forms.CharField(
        label=_("Qualification"),
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    requested_at = forms.DateTimeField(
        required=False,
        label=_("Requested At"),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'readonly': 'readonly'})
    )
    qualification_date = forms.DateField(
        required=False,
        label=_("Qualification Date"),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    expires_at = forms.DateField(
        required=False,
        label=_("Expires At"),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    reason = forms.CharField(
        required=False,
        label=_("Reason for Action"),
        widget=forms.TextInput(attrs={'placeholder': _('Optional reason for action')}),
    )
