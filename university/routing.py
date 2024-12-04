# university_system/routing.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import django_plotly_dash.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab3.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        django_plotly_dash.routing.websocket_urlpatterns
    ),
})