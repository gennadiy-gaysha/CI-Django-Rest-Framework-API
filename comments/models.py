from django.db import models
from django.contrib.auth.models import User
from posts.models import Posts

class Comment(models.Model):
    '''
    Comment model related to User and Posts
    '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE,
                              related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content

