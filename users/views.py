from django.contrib.auth import get_user_model
from rest_framework import status, generics, filters
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema, extend_schema_view

from users.models import Follow
from users.serializers import (
    UserRegistrationSerializer,
    FollowSerializer,
    UserProfileSerializer,
)

User = get_user_model()


@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: {"message": "User created successfully"}},
    tags=["Users"],
    summary="User registration",
    description="Registration of a new user with email, username and password validation"
)
class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        summary="User list",
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="User details",
        tags=["Users"]
    ),
    create=extend_schema(
        summary="Creating a user",
        tags=["Users"]
    ),
    update=extend_schema(
        summary="User update",
        tags=["Users"]
    ),
    partial_update=extend_schema(
        summary="Partial user update",
        tags=["Users"]
    ),
    destroy=extend_schema(
        summary="Deleting a user",
        tags=["Users"]
    ),
)
class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]


@extend_schema(
    summary="Getting the current user's profile",
    tags=["Users"],
    responses={200: UserProfileSerializer}
)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


@extend_schema(
    summary="Subscribe to user",
    tags=["Follows"],
    request=FollowSerializer,
    responses={201: FollowSerializer}
)
class FollowCreateView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


@extend_schema(
    summary="List of current user subscriptions",
    tags=["Follows"],
    responses={200: FollowSerializer(many=True)}
)
class FollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)


@extend_schema(
    summary="Unfollow user",
    tags=["Follows"],
    responses={204: None, 400: {"detail": "Not following this user."}}
)
class UnfollowView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_id")
        follow = Follow.objects.filter(follower=request.user, following_id=user_id).first()
        if follow:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not following this user."}, status=status.HTTP_400_BAD_REQUEST)
