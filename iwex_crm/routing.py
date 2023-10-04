from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from applications.accounts import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.MessageConsumer.as_asgi()),
    path('ws/test/', consumers.TestConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),
})
