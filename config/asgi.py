import os

# 1️⃣ Set the settings module first — must be **before any Django imports**
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# 2️⃣ Now import Django ASGI application
from django.core.asgi import get_asgi_application

# 3️⃣ Import Channels stuff AFTER settings is set
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# 4️⃣ Import your routing AFTER settings is configured
import notifications.routing

# 5️⃣ Initialize Django ASGI app
django_asgi_app = get_asgi_application()

# 6️⃣ Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(notifications.routing.websocket_urlpatterns)
    ),
})