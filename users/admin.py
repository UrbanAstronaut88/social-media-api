from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Follow

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    ordering = ("id",)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following")
    search_fields = ("follower__username", "following__username")
    ordering = ("id",)
