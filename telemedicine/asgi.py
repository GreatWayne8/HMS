"""
ASGI config for telemedicine project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from teleconsultation.routing import websocket_urlpatterns  # Import the WebSocket URL patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telemedicine.settings')

# Django ASGI application to handle HTTP and WebSocket protocols
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # WebSocket routes
        )
    ),
})
