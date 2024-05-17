from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

admin.site.unregister(User)  # Unregister the default User admin
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__email')
