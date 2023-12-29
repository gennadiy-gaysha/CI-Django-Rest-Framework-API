from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Posts
from .serializers import PostsSerializer

class PostsList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged-in user.
    """
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Posts.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()


