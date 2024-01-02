from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Count
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
    queryset = Posts.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter
                       ]
    filterset_fields = [
                        # user feed: showing posts that are owned by users  that
                        # a particular user is following
                        'owner__followed__owner__profile',
                        # showing posts that are liked by a  particular user
                        'likes__owner__profile',
                        # showing posts that are owned by a particular user
                        'owner__profile'
                        # user profiles that  follow a user with a given profile_id
                        ]
    search_fields = ['owner__username', 'title']
    ordering_fields = ['likes_count', 'comments_count', 'likes__created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostsSerializer
    queryset = Posts.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    # Authentication: When you log in to a website by providing your username
    # and password, the system checks whether the provided credentials match a
    # valid user in its database.
    # Authentication is about verifying identity, ensuring that a user is who
    # they claim to be.
    #
    # Authorization: Once authenticated, the system checks your user profile or
    # role to determine what actions you are allowed to perform or what parts of
    # the application you can access. For instance, an admin might have different
    # permissions than a regular user.
    # Authorization is about granting or denying access based on the authenticated
    # user's permissions.
    #
    # JWTs can be used for authentication such as "ID
    # tokens" and also for authorization such as "access tokens".
