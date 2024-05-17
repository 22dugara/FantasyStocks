from django.urls import path
from .views import RegisterView, login_view, logout_view, UserProfileView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
