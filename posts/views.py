from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

from drf_api.permissions import IsOwnerOrReadOnly
from .models import Posts
from .serializers import PostsSerializer


class PostsList(APIView):
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Posts.objects.all()
        serializer = PostsSerializer(posts, many=True,
                                     context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostsSerializer(data=request.data, context={'request':
                                                                     request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostsDetail(APIView):
    serializer_class = PostsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            post = Posts.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Posts.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        # The request object contains information about the current HTTP request,
        # including details about the user making the request, headers, and other
        # request-specific information.
        serializer = PostsSerializer(post, context={
            'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostsSerializer(post, data=request.data,
                                     context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
