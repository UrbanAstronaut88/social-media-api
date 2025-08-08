from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view

from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, LikeSerializer, CommentSerializer


@extend_schema_view(
    list=extend_schema(summary="Post list", description="Get a list of a user's posts and subscriptions"),
    create=extend_schema(summary="Create a post", description="Create a new post as an authorised user"),
    retrieve=extend_schema(summary="Details of the post", description="Get details of a specific post"),
    update=extend_schema(summary="Update post", description="Update post data"),
    partial_update=extend_schema(summary="Partially update post", description="Partial update of the post"),
    destroy=extend_schema(summary="Delete post", description="Delete post"),
)
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        following_ids = user.followings.values_list("following__id", flat=True)
        relevant_ids = list(following_ids) + [user.id]
        return Post.objects.filter(author__id__in=relevant_ids).order_by("-created_at")


@extend_schema(
    summary="Like",
    description="Like the post. You cannot like the same post twice.",
    request=LikeSerializer,
    responses={201: LikeSerializer, 400: None},
)
class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        if Like.objects.filter(user=request.user, post_id=post_id).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data={"post": post_id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Unlike",
    description="Remove a like from a post if it was given by the user.",
    responses={204: None, 404: None},
)
class LikeDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        like = Like.objects.filter(user=request.user, post_id=post_id).first()
        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    list=extend_schema(summary="List of comments", description="Get a list of comments on the post"),
    create=extend_schema(summary="Add a comment", description="Add a new comment to the post"),
)
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(user=self.request.user, post_id=post_id)
