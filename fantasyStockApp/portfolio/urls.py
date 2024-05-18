from django.urls import path
from .views import portfolio_management

urlpatterns = [
    path('management/', portfolio_management, name='portfolio_management'),
]
