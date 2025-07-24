from django.utils.translation import gettext_lazy as _
from django import forms
from ephios.core.models import Qualification
from .models import QualificationRequest, QualificationDefaultExpirationTime

class QualificationSubmitForm(forms.ModelForm):
    qualification = forms.ModelChoiceField(
        queryset=Qualification.objects.all(),
        required=True,
        label=_("Qualification"),
        widget=forms.Select(attrs={"placeholder": _("Select Qualification")})
    )
    qualification_date = forms.DateField(
        required=True,
        label=_("Qualification Date"),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    image = forms.ImageField(
        required=True,
        label=_("Upload Image"),
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = QualificationRequest
        fields = ['qualification', 'qualification_date']

class QualificationDetailForm(forms.Form):
    user = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )
    qualification = forms.CharField(
        required=True,
        widget=forms.HiddenInput()
    )
    requested_at = forms.DateTimeField(
        required=False,
        widget=forms.HiddenInput()
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
        label=_("Optional Reason for Action"),
        widget=forms.TextInput(attrs={'placeholder': _('Reason')}),
    )
    qualification_default_expiration_time_days = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
    qualification_default_expiration_time_years = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )

class QualificationDefaultExpirationTimeAddForm(forms.ModelForm):
    qualification = forms.ModelChoiceField(
        queryset=Qualification.objects.all(),
        required=True,
        label=_("Qualification"),
        widget=forms.Select(attrs={"placeholder": _("Select Qualification")})
    )
    default_expiration_time_years = forms.IntegerField(
        required=True,
        label=_("Years"),
        widget=forms.NumberInput(attrs={'min': 0, 'placeholder': _("Years")})
    )
    default_expiration_time_days = forms.IntegerField(
        required=True,
        label=_("Days"),
        widget=forms.NumberInput(attrs={'min': 0, 'placeholder': _("Days")})
    )

    class Meta:
        model = QualificationDefaultExpirationTime
        fields = ['qualification', 'default_expiration_time_years', 'default_expiration_time_days']

class QualificationDefaultExpirationTimeDetailForm(forms.ModelForm):
    qualification = forms.ModelChoiceField(
        queryset=Qualification.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )
    default_expiration_time_years = forms.IntegerField(
        required=True,
        label=_("Years"),
        widget=forms.NumberInput(attrs={'min': 0, 'placeholder': _("Years")})
    )
    default_expiration_time_days = forms.IntegerField(
        required=True,
        label=_("Days"),
        widget=forms.NumberInput(attrs={'min': 0, 'placeholder': _("Days")})
    )

    class Meta:
        model = QualificationDefaultExpirationTime
        fields = ['qualification', 'default_expiration_time_years', 'default_expiration_time_days']
