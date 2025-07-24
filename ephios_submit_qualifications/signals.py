from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.dispatch import receiver
from ephios.core.signals import (
    settings_sections,
    register_group_permission_fields,
)
from ephios.core.views.settings import SETTINGS_MANAGEMENT_SECTION_KEY, SETTINGS_PERSONAL_SECTION_KEY
from ephios.extra.permissions import PermissionField

@receiver(settings_sections)
def add_navigation_item(sender, request, **kwargs):
    user = request.user

    sections = []

    if user.is_authenticated and user.has_perm('ephios_submit_qualifications.view_own_qualification_requests'):
        sections.append(
            {
                "label": _("Own Qualification Requests"),
                "url": reverse("ephios_submit_qualifications:own_qualification_requests"),
                "group": SETTINGS_PERSONAL_SECTION_KEY,
                "active": request.path.startswith(reverse("ephios_submit_qualifications:own_qualification_requests")),
            }
        )
    
    if user.is_authenticated and user.has_perm('ephios_submit_qualifications.view_qualification_requests'):
        sections.append(
            {
                "label": _("Manage Qualification Requests"),
                "url": reverse("ephios_submit_qualifications:qualification_requests"),
                "group": SETTINGS_MANAGEMENT_SECTION_KEY,
                "active": request.path.startswith(reverse("ephios_submit_qualifications:qualification_requests")),
            }
        )

    if user.is_authenticated and user.has_perm('ephios_submit_qualifications.view_qualification_default_expiration_time'):
        sections.append(
            {
                "label": _("Qualification Default Expiration Times"),
                "url": reverse("ephios_submit_qualifications:qualification_default_expiration_time_list"),
                "group": SETTINGS_MANAGEMENT_SECTION_KEY,
                "active": request.path.startswith(reverse("ephios_submit_qualifications:qualification_default_expiration_time_list")),
            }
        )

    return sections

@receiver(register_group_permission_fields)
def register_permission_fields(sender, **kwargs):
    return [
        (
            "submit_qualification_requests",
            PermissionField(
                label=_("Submit Qualification Requests"),
                help_text=_("Allows to submit qualification requests."),
                permissions=[
                    "ephios_submit_qualifications.add_qualification_request",
                    "ephios_submit_qualifications.view_own_qualification_requests",
                ],
            ),
        ),
        (
            "manage_qualification_requests",
            PermissionField(
                label=_("Manage Qualification Requests"),
                help_text=_("Allows to manage qualification requests."),
                permissions=[
                    "ephios_submit_qualifications.view_qualification_requests",
                    "ephios_submit_qualifications.view_qualification_request_details",
                    "ephios_submit_qualifications.manage_qualification_requests",
                ],
            ),
        ),
        (
            "manage_own_qualification_requests",
            PermissionField(
                label=_("Manage Own Qualification Requests"),
                help_text=_("Allows to manage own qualification requests to."),
                permissions=[
                    "ephios_submit_qualifications.manage_own_qualification_requests",
                ],
            ),
        ),
        (
            "manage_qualification_default_expiration_times",
            PermissionField(
                label=_("Manage Qualification Default Expiration Times"),
                help_text=_("Allows to manage default expiration times for qualifications."),
                permissions=[
                    "ephios_submit_qualifications.view_qualification_default_expiration_time",
                    "ephios_submit_qualifications.add_qualification_default_expiration_time",
                    "ephios_submit_qualifications.change_qualification_default_expiration_time",
                    "ephios_submit_qualifications.delete_qualification_default_expiration_time",
                ],
            )
        )
    ]
