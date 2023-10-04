# core/management/commands/run_ws_server.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.management.base import BaseCommand
from django.urls import path
from channels.layers import get_channel_layer
from channels.middleware import MiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from core.consumers import VacancyConsumer
from asgiref.wsgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": VacancyConsumer.as_asgi(),
})

class Command(BaseCommand):
    help = "Run WebSocket server"

    def handle(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        channel_layer.channel_name = "default"

        application = ProtocolTypeRouter({
            "http": get_asgi_application(),
            "websocket": VacancyConsumer.as_asgi(),
        })

        application(scope={"type": "websocket.connect"})
