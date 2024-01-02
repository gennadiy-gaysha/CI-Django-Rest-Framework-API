from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend

class CommentList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    filter_backends = [DjangoFilterBackend]
    # retrieve all the comments associated with a given post
    filterset_fields = ['posts']

    # Before we test the view, we’ll have to make sure  comments are associated
    # with a user upon creation.
    # We do this with generics by defining the perform_create method,
    # which takes in self and serializer as arguments.  Inside, we pass in the
    # user making the request as owner into the serializer’s 'save' method, just
    # like we did in the regular class based views.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()



