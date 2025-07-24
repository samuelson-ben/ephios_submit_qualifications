from django.utils.translation import gettext_lazy as _
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.utils.timezone import localtime
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from ephios.core.models import QualificationGrant
from .forms import (
    QualificationSubmitForm,
    QualificationDetailForm,
    QualificationDefaultExpirationTimeAddForm,
    QualificationDefaultExpirationTimeDetailForm
)
from .models import (
    QualificationRequest,
    QualificationDefaultExpirationTime
)
from .notifications import (
    QualificationRequestAcceptedNotification,
    QualificationRequestRejectedNotification,
)

class OwnQualificationRequestView(LoginRequiredMixin, TemplateView):
    template_name = "ephios_submit_qualifications/qualification_requests/own_list.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to view qualification requests.")
        if not user.has_perm('ephios_submit_qualifications.view_own_qualification_requests'):
            raise PermissionDenied("You do not have permission to view your own qualification requests.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualification_requests'] = QualificationRequest.objects.filter(user=self.request.user)
        context['can_submit'] = self.request.user.has_perm('ephios_submit_qualifications.add_qualification_request')
        return context

class QualificationSubmitView(LoginRequiredMixin, FormView):
    template_name = "ephios_submit_qualifications/qualification_requests/add_form.html"
    form_class = QualificationSubmitForm
    success_url = reverse_lazy("ephios_submit_qualifications:own_qualification_requests")

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to submit qualifications.")
        if not user.has_perm('ephios_submit_qualifications.add_qualification_request'):
            raise PermissionDenied("You do not have permission to submit qualifications.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        upload_image = form.cleaned_data.get('image', None)
        if upload_image:
            image_data = upload_image.read()
            image_content_type = upload_image.content_type
        else:
            image_data = None
            image_content_type = None

        QualificationRequest.objects.create(
            user=self.request.user,
            qualification=form.cleaned_data['qualification'],
            qualification_date=form.cleaned_data['qualification_date'],
            image_data=image_data,
            image_content_type=image_content_type
        )

        return super().form_valid(form)

class QualificationRequestsView(LoginRequiredMixin, TemplateView):
    template_name = "ephios_submit_qualifications/qualification_requests/list.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to view qualification requests.")
        if not user.has_perm('ephios_submit_qualifications.view_qualification_requests'):
            raise PermissionDenied("You do not have permission to view qualification requests.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualification_requests'] = QualificationRequest.objects.all()
        return context

class QualificationRequestDetailView(LoginRequiredMixin, FormView):
    template_name = "ephios_submit_qualifications/qualification_requests/details_form.html"
    form_class = QualificationDetailForm
    success_url = reverse_lazy("ephios_submit_qualifications:qualification_requests")

    def dispatch(self, request, *args, **kwargs):
        self.qualification_request = get_object_or_404(QualificationRequest, pk=kwargs['pk'])
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to view this request.")
        if user == self.qualification_request.user and not user.has_perm('ephios_submit_qualifications.view_own_qualification_requests'):
            raise PermissionDenied("You do not have permission to view your own request images.")
        if user != self.qualification_request.user and not user.has_perm('ephios_submit_qualifications.view_qualification_request_details'):
            raise PermissionDenied("You do not have permission to view this request.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualification_request'] = self.qualification_request
        context['is_own_request'] = self.request.user == self.qualification_request.user
        context['can_manage_own_request'] = self.request.user.has_perm('ephios_submit_qualifications.manage_own_qualification_requests')
        return context

    def get_initial(self):
        qualification_request = self.qualification_request
        expiration_time = None
        qualification_default_expiration_time = QualificationDefaultExpirationTime.objects.filter(
            qualification=qualification_request.qualification
        ).first()
        if qualification_default_expiration_time:
            expiration_time = qualification_request.qualification_date + relativedelta(
                years=qualification_default_expiration_time.default_expiration_time_years,
                days=qualification_default_expiration_time.default_expiration_time_days
            )
        return {
            'user': qualification_request.user.get_full_name(),
            'qualification': str(qualification_request.qualification),
            'qualification_date': qualification_request.qualification_date.strftime('%Y-%m-%d'),
            'requested_at': localtime(qualification_request.requested_at).strftime('%Y-%m-%dT%H:%M'),
            'expires_at': expiration_time.strftime('%Y-%m-%d') if expiration_time else None,
            'reason': '',
            'qualification_default_expiration_time_days': qualification_default_expiration_time.default_expiration_time_days if qualification_default_expiration_time else None,
            'qualification_default_expiration_time_years': qualification_default_expiration_time.default_expiration_time_years if qualification_default_expiration_time else None
        }
    
    def form_valid(self, form):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to manage qualification requests.")
        if not user.has_perm('ephios_submit_qualifications.manage_qualification_requests'):
            raise PermissionDenied("You do not have permission to manage qualification requests.")
        if user == self.qualification_request.user and not user.has_perm('ephios_submit_qualifications.manage_own_qualification_requests'):
            raise PermissionDenied("You do not have permission to manage your own requests.")
        
        reason = form.cleaned_data.get('reason', None)
        if "approve" in self.request.POST:
            expires_at = form.cleaned_data.get('expires_at')
            if expires_at:
                expires_at = datetime.combine(expires_at, time(23, 59))
            grant, created = QualificationGrant.objects.get_or_create(
                user=self.qualification_request.user,
                qualification=self.qualification_request.qualification,
                defaults={'expires': expires_at}
            )
            if not created:
                grant.expires = form.cleaned_data.get('expires_at')
                grant.save()
            QualificationRequestAcceptedNotification.send(self, reason)
            self.qualification_request.delete()
        elif "deny" in self.request.POST:
            QualificationRequestRejectedNotification.send(self, reason)
            self.qualification_request.delete()
        return super().form_valid(form)

@login_required
def qualification_request_image(request, pk):
    qr = get_object_or_404(QualificationRequest, pk=pk)
    
    user = request.user
    if not user.is_authenticated:
        raise PermissionDenied("You do not have permission to view this image.")
    if user == qr.user and not user.has_perm('ephios_submit_qualifications.view_own_qualification_requests'):
        raise PermissionDenied("You do not have permission to view your own request images.")
    if user != qr.user and not user.has_perm('ephios_submit_qualifications.view_qualification_request_details'):
        raise PermissionDenied("You do not have permission to view this request image.")
    
    return HttpResponse(
        qr.image_data,
        content_type=qr.image_content_type or 'application/octet-stream'
    )

class QualificationDefaultExpirationTimeListView(LoginRequiredMixin, TemplateView):
    template_name = "ephios_submit_qualifications/qualification_default_expiration_time/list.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to view default expiration times.")
        if not user.has_perm('ephios_submit_qualifications.view_qualification_default_expiration_time'):
            raise PermissionDenied("You do not have permission to view default expiration times.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_expiration_times'] = QualificationDefaultExpirationTime.objects.all()
        context['can_add'] = self.request.user.has_perm('ephios_submit_qualifications.add_qualification_default_expiration_time')
        return context

class QualificationDefaultExpirationTimeAddView(LoginRequiredMixin, FormView):
    template_name = "ephios_submit_qualifications/qualification_default_expiration_time/add_form.html"
    form_class = QualificationDefaultExpirationTimeAddForm
    success_url = reverse_lazy("ephios_submit_qualifications:qualification_default_expiration_time_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to add default expiration times.")
        if not user.has_perm('ephios_submit_qualifications.add_qualification_default_expiration_time'):
            raise PermissionDenied("You do not have permission to add default expiration times.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if QualificationDefaultExpirationTime.objects.filter(
            qualification=form.cleaned_data['qualification']
        ).exists():
            form.add_error('qualification', _("A default expiration time for this qualification already exists."))
            return self.form_invalid(form)
        form.save()
        return super().form_valid(form)

class QualificationDefaultExpirationTimeDetailView(LoginRequiredMixin, FormView):
    template_name = "ephios_submit_qualifications/qualification_default_expiration_time/details_form.html"
    form_class = QualificationDefaultExpirationTimeDetailForm
    success_url = reverse_lazy("ephios_submit_qualifications:qualification_default_expiration_time_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualification'] = self.default_expiration_time.qualification
        context['can_change'] = self.request.user.has_perm('ephios_submit_qualifications.change_qualification_default_expiration_time')
        context['can_delete'] = self.request.user.has_perm('ephios_submit_qualifications.delete_qualification_default_expiration_time')
        return context

    def dispatch(self, request, *args, **kwargs):
        self.default_expiration_time = get_object_or_404(QualificationDefaultExpirationTime, pk=kwargs['pk'])
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to view this default expiration time.")
        if not user.has_perm('ephios_submit_qualifications.view_qualification_default_expiration_time'):
            raise PermissionDenied("You do not have permission to change default expiration times.")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {
            'qualification': self.default_expiration_time.qualification,
            'default_expiration_time_years': self.default_expiration_time.default_expiration_time_years,
            'default_expiration_time_days': self.default_expiration_time.default_expiration_time_days
        }

    def form_valid(self, form):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to manage default expiration times.")
        if not user.has_perm('ephios_submit_qualifications.change_qualification_default_expiration_time') or not user.has_perm('ephios_submit_qualifications.delete_qualification_default_expiration_time'):
            raise PermissionDenied("You do not have permission to manage default expiration times.")
        
        if "save" in self.request.POST:
            if not user.has_perm('ephios_submit_qualifications.change_qualification_default_expiration_time'):
                raise PermissionDenied("You do not have permission to change default expiration times.")
            form.instance.pk = self.default_expiration_time.pk
            form.save()
        elif "delete" in self.request.POST:
            if not user.has_perm('ephios_submit_qualifications.delete_qualification_default_expiration_time'):
                raise PermissionDenied("You do not have permission to delete default expiration times.")
            self.default_expiration_time.delete()
        return super().form_valid(form)