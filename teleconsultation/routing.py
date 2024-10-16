from django.urls import re_path
from . import consumers  # We'll create this consumer next

websocket_urlpatterns = [
    re_path(r'ws/teleconsultation/(?P<teleconsultation_id>\w+)/$', consumers.TeleconsultationConsumer.as_asgi()),
]
