from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, TemplateView
from django.urls import reverse_lazy
from ephios.core.models import QualificationGrant
from .forms import QualificationSubmitForm, QualificationDetailForm
from .models import QualificationRequest

class QualificationSubmitView(LoginRequiredMixin, FormView):
    template_name = "ephios_submit_qualifications/qualification_submit_form.html"
    form_class = QualificationSubmitForm
    success_url = reverse_lazy("core:settings_personal_data")

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        QualificationRequest.objects.create(
            user=self.request.user,
            qualification=form.cleaned_data['qualification'],
            qualification_date=form.cleaned_data['qualification_date']
        )

        return super().form_valid(form)

class QualificationRequestsView(LoginRequiredMixin, TemplateView):
    template_name = "ephios_submit_qualifications/qualification_requests.html"

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualification_requests'] = QualificationRequest.objects.all()
        return context

class QualificationRequestDetailView(LoginRequiredMixin, FormView):
    template_name = "ephios_submit_qualifications/qualification_request_detail.html"
    form_class = QualificationDetailForm
    success_url = reverse_lazy("ephios_submit_qualifications:qualification_requests")

    def dispatch(self, request, *args, **kwargs):
        self.qualification_request = get_object_or_404(QualificationRequest, pk=kwargs['pk'])
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied("You do not have permission to view this request.")
        if not user.is_staff and (user is self.qualification_request.user):
            raise PermissionDenied("You do not have permission to view this request.")
        if user.is_staff or user.has_perm('core.change_qualification'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("An unexpected error occurred.")

    def get_initial(self):
        qr = self.qualification_request
        return {
            'user': qr.user.get_full_name(),
            'qualification': str(qr.qualification),
            'qualification_date': qr.qualification_date,
            'requested_at': localtime(qr.requested_at),
            'expires_at': None,
            'reason': ''
        }        
    
    def form_valid(self, form):
        if "approve" in self.request.POST:
            QualificationGrant.objects.create(
                user=self.qualification_request.user,
                qualification=self.qualification_request.qualification,
                qualification_date=self.qualification_request.qualification_date
            )
            self.qualification_request.delete()
        elif "deny" in self.request.POST:
            self.qualification_request.delete()
        return super().form_valid(form)