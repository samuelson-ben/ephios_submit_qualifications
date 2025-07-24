from django.db import models
from django.conf import settings
from ephios.core.models import Qualification
from logging import getLogger
import os

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
    image_data = models.BinaryField(null=True, blank=True)
    image_content_type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Qualification Request"
        verbose_name_plural = "Qualification Requests"
        ordering = ['-requested_at']
        permissions = [
            ("view_own_qualification_requests", "Can view own qualification requests"),
            ("view_qualification_requests", "Can view all qualification requests"),
            ("view_qualification_request_details", "Can view qualification request details"),
            ("add_qualification_request", "Can add qualification requests"),
            ("manage_qualification_requests", "Can manage qualification requests"),
            ("manage_own_qualification_requests", "Can manage own qualification requests"),
        ]

    def __str__(self):
        return f"{self.user} requested {self.qualification} on {self.requested_at}"

class QualificationDefaultExpirationTime(models.Model):
    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        related_name='default_expiration_times',
    )
    default_expiration_time_years = models.IntegerField(
        default=0,
    )
    default_expiration_time_days = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = "Qualification Default Expiration Time"
        verbose_name_plural = "Qualification Default Expiration Times"
        ordering = ['qualification']
        permissions = [
            ("view_qualification_default_expiration_time", "Can view qualification default expiration times"),
            ("add_qualification_default_expiration_time", "Can add qualification default expiration times"),
            ("change_qualification_default_expiration_time", "Can change qualification default expiration times"),
            ("delete_qualification_default_expiration_time", "Can delete qualification default expiration times"),
        ]

    def __str__(self):
        return f"{self.qualification} - {self.default_expiration_time_years} years, {self.default_expiration_time_days} days"
