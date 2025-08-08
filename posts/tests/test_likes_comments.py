from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Like, Comment

User = get_user_model()


class LikeCommentTests(APITestCase):
    def setUp(self):
        # creating a user
        self.user = User.objects.create_user(email="test@example.com", username="testuser", password="testpass123")

        # get a JWT token
        response = self.client.post("/api/token/", {"email": "test@example.com", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        token = response.data["access"]

        # set token in headers
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # creating a post
        self.post = Post.objects.create(author=self.user, content="Test Post")

    def test_like_post(self):
        url = reverse("like-create", kwargs={"post_id": self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get().user, self.user)

    def test_like_post_twice_fails(self):
        url = reverse("like-create", kwargs={"post_id": self.post.id})
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_post(self):
        # Like the post first
        Like.objects.create(user=self.user, post=self.post)
        url = reverse("like-delete", kwargs={"post_id": self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_comment_create_and_list(self):
        url = reverse("comment-list-create", kwargs={"post_id": self.post.id})

        # creating comment
        data = {"content": "Nice post!"}
        response = self.client.post(url, data)
#       print("RESPONSE DATA:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "Nice post!")

        # verifying list receipt
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "Nice post!")
