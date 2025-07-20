from ephios.core.plugins import PluginConfig


class PluginApp(PluginConfig):
    name = "ephios_submit_qualifications"

    class EphiosPluginMeta:
        name = "ephios_submit_qualifications"
        author = "Ben Samuelson <ben.samuelson@fiteka.de>"
        description = "Users can submit requests to gain qualifications"

    def ready(self):
        from . import signals  # NOQA
