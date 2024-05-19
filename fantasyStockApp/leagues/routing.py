from django.urls import path
from .consumers import LeagueConsumer

websocket_urlpatterns = [
    path('ws/league/<str:league_name>/', LeagueConsumer.as_asgi()),
]
