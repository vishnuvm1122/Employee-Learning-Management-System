from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.timezone import now
from django.template.defaultfilters import timesince
from .models import Notification

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    """
    Sends a WebSocket message to the receiver's group when a **new Notification is created**.
    Only relevant for unread notifications.
    """
    if created and not instance.is_read:
        channel_layer = get_channel_layer()
        group_name = f"notifications_{instance.receiver.id}"

        # The consumer will fetch the latest unread notifications,
        # so the payload can be minimal or empty.
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",  # Matches the consumer method
            }
        )