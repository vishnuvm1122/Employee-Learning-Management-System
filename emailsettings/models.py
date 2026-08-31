from django.db import models
from django.conf import settings

class EmailSettings(models.Model):
    host = models.CharField(max_length=255, blank=True, null=True)
    port = models.PositiveIntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    use_tls = models.BooleanField(default=False)
    use_ssl = models.BooleanField(default=False)

    email_enabled = models.BooleanField(
        default=True,
        help_text="Turn email sending ON or OFF."
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Email Settings"

    class Meta:
        verbose_name = "Email Settings"
        verbose_name_plural = "Email Settings"
        
        
class SendEmailToReceiveUsers(models.Model):
    """
    Store users who should be notified (email NOT sent yet).
    """
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="pending_notifications",
        blank=True,
        help_text="Users who are selected for notification"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Send Email To Receive User"
        verbose_name_plural = "Send Email To Receive Users"
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification record ({self.users.count()} users)"