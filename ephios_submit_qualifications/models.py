from django.db import models
from django.conf import settings
from ephios.core.models import Qualification

class QualificationRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='qualification_requests',
    )
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
    )
    qualification_date = models.DateField(null=False, blank=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Qualification Request"
        verbose_name_plural = "Qualification Requests"
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.user} requested {self.qualification} on {self.requested_at}"
