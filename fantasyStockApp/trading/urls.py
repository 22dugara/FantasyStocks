from django.urls import path
from .views import transact

urlpatterns = [
    path('transact/', transact, name='transact'),
]

