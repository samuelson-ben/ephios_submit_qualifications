from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.dispatch import receiver
from ephios.core.signals import settings_sections
from ephios.core.views.settings import SETTINGS_MANAGEMENT_SECTION_KEY, SETTINGS_PERSONAL_SECTION_KEY

@receiver(settings_sections)
def add_navigation_item(sender, request, **kwargs):
    user = request.user

    sections = []
    
    if user.is_authenticated:
        sections.append(
            {
                "label": _("Submit Qualifications"),
                "url": reverse("ephios_submit_qualifications:qualification_submit_form"),
                "group": SETTINGS_PERSONAL_SECTION_KEY,
                "active": request.path.startswith(reverse("ephios_submit_qualifications:qualification_submit_form")),
            }
        )
    
    if user.is_authenticated and (user.is_staff or user.has_perm('core.change_qualification')):
        sections.append(
            {
                "label": _("Manage Qualification Requests"),
                "url": reverse("ephios_submit_qualifications:qualification_requests"),
                "group": SETTINGS_MANAGEMENT_SECTION_KEY,
                "active": request.path.startswith(reverse("ephios_submit_qualifications:qualification_requests")),
            }
        )

    return sections
