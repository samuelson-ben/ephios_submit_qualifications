from django.conf import settings
from django.urls import path
from .views import (
    OwnQualificationRequestView,
    QualificationSubmitView,
    QualificationRequestsView,
    QualificationRequestDetailView,
    qualification_request_image
)

app_name = "ephios_submit_qualifications"

urlpatterns = [
    path(
        "settings/qualifications/own/",
        OwnQualificationRequestView.as_view(),
        name="own_qualification_requests",
    ),
    path(
        "settings/qualifications/own/submit/",
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
    path(
        "settings/qualifications/requests/<int:pk>/image/",
        qualification_request_image,
        name="qualification_request_image",
    ),
]