from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet, LikeCreateView, LikeDeleteView, CommentListCreateView

router = DefaultRouter()
router.register(r"", PostViewSet, basename="posts")  # available at api/posts/

urlpatterns = [
    path("", include(router.urls)),  # ViewSet (PostViewSet)

    # likes and comments
    path("<int:post_id>/like/", LikeCreateView.as_view(), name="like-create"),
    path("<int:post_id>/unlike/", LikeDeleteView.as_view(), name="like-delete"),
    path("<int:post_id>/comments/", CommentListCreateView.as_view(), name="comment-list-create"),
]
