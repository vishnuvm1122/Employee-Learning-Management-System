import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            await self.send_notifications()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass  # Optional: handle messages from frontend

    async def send_notification(self, event):
        """Called from signals via channel_layer.group_send"""
        await self.send_notifications()

    async def send_notifications(self):
        from .models import Notification  # lazy import

        # Fetch **only unread notifications**
        notifications, unread_count = await sync_to_async(self._fetch_unread_notifications)()

        notif_list = []
        for n in notifications:
            sender_name = n.sender.get_full_name if n.sender else "System"
            notif_list.append({
                "id": n.id,
                "sender": sender_name or getattr(n.sender, 'username', 'System'),
                "message": n.message,
                "url": getattr(n, "url", "#"),
                "time_since": timesince(n.created_at) + " ago",
            })

        payload = {
            "count": unread_count,       # only unread count
            "notifications": notif_list, # only unread notifications
        }

        await self.send(text_data=json.dumps(payload))

    def _fetch_unread_notifications(self):
        """Fetch latest 5 unread notifications and unread count"""
        from .models import Notification

        # Latest 5 unread notifications
        notifications = list(
            Notification.objects.select_related("sender")
            .filter(receiver=self.user, is_read=False)
            .order_by("-created_at")[:5]
        )

        unread_count = len(notifications)  # same as count of unread

        return notifications, unread_count