from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ephios.core.models.users import Consequence, Notification
from ephios.core.services.notifications.types import AbstractNotificationHandler

def register_notifications(sender, **kwargs):
    return [
        QualificationRequestAcceptedNotification,
        QualificationRequestRejectedNotification,
        QualificationRequestCreateNotification,
    ]

class QualificationRequestAcceptedNotification(AbstractNotificationHandler):
    slug = "qualification_request_accepted"
    title = _("Qualification Request Accepted")

    @classmethod
    def send(cls, consequence: Consequence, reason=None):
        qualification_request = consequence.qualification_request
        Notification.objects.create(
            slug=cls.slug,
            user=qualification_request.user,
            data={
                "qualificationtitle": getattr(qualification_request.qualification, 'title', _('Unknown Qualification')),
                "reason": reason,
            },
        )

    @classmethod
    def get_subject(cls, notification):
        return _("Qualification Request Accepted")
    
    @classmethod
    def get_body(cls, notification):
        base_text = _(
            "Your qualification request for {qualification} has been accepted."
        ).format(
            qualification=notification.data.get('qualificationtitle', _('Unknown Qualification')),
        )
        reason = notification.data.get('reason', None)
        if reason:
            base_text += "\n" + _("Reason: {reason}").format(reason=reason)
        return base_text
    
    @classmethod
    def as_html(cls, notification):
        return """
            <p><strong>{subject}</strong></p>
            <p>{body}</p>
        """.format(
            subject=cls.get_subject(notification),
            body=cls.get_body(notification),
        )
    
    @classmethod
    def get_url(cls, notification):
        return reverse("core:settings_personal_data")

class QualificationRequestRejectedNotification(AbstractNotificationHandler):
    slug = "qualification_request_rejected"
    title = _("Qualification Request Rejected")

    @classmethod
    def send(cls, consequence: Consequence, reason=None):
        qualification_request = consequence.qualification_request
        Notification.objects.create(
            slug=cls.slug,
            user=qualification_request.user,
            data={
                "qualificationtitle": getattr(qualification_request.qualification, 'title', _('Unknown Qualification')),
                "reason": reason,
            },
        )

    @classmethod
    def get_subject(cls, notification):
        return _("Qualification Request Rejected")
    
    @classmethod
    def get_body(cls, notification):
        base_text = _(
            "Your qualification request for {qualification} has been rejected."
        ).format(
            qualification=notification.data.get('qualificationtitle', _('Unknown Qualification')),
        )
        reason = notification.data.get('reason', None)
        if reason:
            base_text += "\n" + _("Reason: {reason}").format(reason=reason)
        return base_text
        
    
    @classmethod
    def as_html(cls, notification):
        return """
            <p><strong>{subject}</strong></p>
            <p>{body}</p>
        """.format(
            subject=cls.get_subject(notification),
            body=cls.get_body(notification).replace("\n", "<br>"),
        )
    
    @classmethod
    def get_url(cls, notification):
        return reverse("core:settings_personal_data")

class QualificationRequestCreateNotification(AbstractNotificationHandler):
    slug = "qualification_request_created"
    title = _("Qualification Request Created")

    @classmethod
    def send(cls, user, qualification_request):
        Notification.objects.create(
            slug=cls.slug,
            user=user,
            data={
                "username": qualification_request.user.get_full_name() or _('Unknown Username'),
            },
        )

    @classmethod
    def get_subject(cls, notification):
        return _("Qualification Request Created")
    
    @classmethod
    def get_body(cls, notification):
        base_text = _(
            "{username} created a new qualification request."
        ).format(
            username=notification.data.get('username', _('Unknown Username')),
        )
        return base_text
    
    @classmethod
    def as_html(cls, notification):
        return """
            <p><strong>{subject}</strong></p>
            <p>{body}</p>
        """.format(
            subject=cls.get_subject(notification),
            body=cls.get_body(notification),
        )
    
    @classmethod
    def get_url(cls, notification):
        return reverse("ephios_submit_qualifications:qualification_requests")