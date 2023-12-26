from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
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