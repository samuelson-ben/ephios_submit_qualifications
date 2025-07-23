from django.utils.translation import gettext_lazy as _
from ephios.core.plugins import PluginConfig

class PluginApp(PluginConfig):
    name = "ephios_submit_qualifications"

    class EphiosPluginMeta:
        name = _("Qualifications submiting")
        author = "Ben Samuelson <ben.samuelson@fiteka.de>"
        description = _("Users can submit requests to gain qualifications.")

    def ready(self):
        from . import signals  # NOQA

        from ephios.core.signals import register_notification_types
        from .notifications import register_notifications
        register_notification_types.connect(register_notifications, dispatch_uid="ephios_submit_qualifications.register_notifications")
