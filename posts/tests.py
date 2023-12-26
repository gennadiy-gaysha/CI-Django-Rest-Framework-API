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

class PostsDetailViewTests(APITestCase):
    def setUp(self):
        gena = User.objects.create_user(username='gena', password='pass')
        adam = User.objects.create_user(username='adam', password='pass')
        Posts.objects.create(owner=gena, title='a title', content="gena's "
                                                                   "content")
        Posts.objects.create(owner=adam, title='a title', content="adams's "
                                                                   "content")
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='gena', password='pass')
        response=self.client.put('/posts/1/', {'title': 'updated title'})
        post = Posts.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'updated title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_others_post(self):
        self.client.login(username='gena', password='pass')
        response=self.client.put('/posts/2/', {'title': 'updated title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

