from django.utils.translation import gettext_lazy as _
from ephios.core.plugins import PluginConfig

class PluginApp(PluginConfig):
    name = "ephios_submit_qualifications"

    class EphiosPluginMeta:
        name = _("Qualifications submiting")
        author = "Ben Samuelson <ben.samuelson@fiteka.de>"
        description = _("Users can submit requests to gain qualifications")

    def ready(self):
        from . import signals  # NOQA
