from django.urls import path
from .views import QualificationSubmitView, QualificationRequestsView, QualificationRequestDetailView

app_name = "ephios_submit_qualifications"

urlpatterns = [
    path(
        "settings/qualifications/submit/",
        QualificationSubmitView.as_view(),
        name="qualification_submit_form",
    ),
    path(
        "settings/qualifications/requests/",
        QualificationRequestsView.as_view(),
        name="qualification_requests",
    ),
    path(
        "settings/qualifications/requests/<int:pk>/",
        QualificationRequestDetailView.as_view(),
        name="qualification_request_detail",
    ),
]