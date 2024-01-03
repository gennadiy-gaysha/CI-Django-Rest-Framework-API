from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)

@api_view(['GET'])
def root_route(request):
    api_urls = {
        'ProfileList': 'http://127.0.0.1:8000/profiles/',
        'ProfileDetailUpdateDelete': 'http://127.0.0.1:8000/profiles/3/',

        'PostsCreateList': 'http://127.0.0.1:8000/posts/',
        'PostsDetailUpdateDelete': 'http://127.0.0.1:8000/posts/3/',

        'CommentCreateList': 'http://127.0.0.1:8000/comments/',
        'CommentDetailUpdateDelete': 'http://127.0.0.1:8000/comments/3/',

        'LikeCreateList': 'http://127.0.0.1:8000/likes/',
        'LikeDetailUpdateDelete': 'http://127.0.0.1:8000/likes/3/',

        'Registration': 'http://127.0.0.1:8000/registration/',
        'Login': 'http://127.0.0.1:8000/login/',
        'Logout': 'http://127.0.0.1:8000/logout/',
        'User': 'http://127.0.0.1:8000/user/',
        'Refresh Token': 'http://127.0.0.1:8000/token/refresh/',
    }
    return Response(api_urls)

# dj-rest-auth logout view fix
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response