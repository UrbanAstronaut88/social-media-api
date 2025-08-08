from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import (
    UserRegistrationView,
    UnfollowView,
    FollowCreateView,
    UserProfileView,
    FollowListView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")  # available at api/users/

urlpatterns = [
    path("me/", UserProfileView.as_view(), name="user-profile"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("follows/", FollowListView.as_view(), name="follow-list"),
    path("follows/create/", FollowCreateView.as_view(), name="follow-create"),
    path("unfollow/<int:user_id>/", UnfollowView.as_view(), name="unfollow"),

    path("", include(router.urls)),
]
