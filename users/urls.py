from django.urls import path
from .views import UserRegistrationView, FollowView, UnfollowView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("follow/", FollowView.as_view(), name="follow"), # GET, POST
    path("unfollow/<int:following_id>/", UnfollowView.as_view(), name="unfollow"), # DELETE

]