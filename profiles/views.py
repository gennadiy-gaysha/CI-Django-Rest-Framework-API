from django.db.models import Count

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'ProfileCreateList': 'http://127.0.0.1:8000/profiles/',
        'ProfileDetailUpdateDelete': 'http://127.0.0.1:8000/profiles/3/',
        'PostsCreateList': 'http://127.0.0.1:8000/posts/',
        'PostsDetailUpdateDelete': 'http://127.0.0.1:8000/posts/3/',
    }
    return Response(api_urls)

class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        posts_count = Count('owner__posts', distinct=True),
        followers_count = Count('owner__followed', distinct=True),
        following_count = Count('owner__following', distinct=True),
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    # user profiles that  follow a user with a given profile_id
    filterset_fields = ['owner__following__followed__profile']

    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__posts', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
