from django.contrib.auth.models import User
from .models import Posts
from rest_framework.test import APITestCase
from rest_framework import status

class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='gena', password='pass')

    def test_can_list_posts(self):
        gena = User.objects.get(username='gena')
        Posts.objects.create(owner=gena, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='gena', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Posts.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        # self.client.logout()
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
