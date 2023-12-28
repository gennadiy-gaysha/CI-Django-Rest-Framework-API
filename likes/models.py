from django.db import models
from django.contrib.auth.models import User
from posts.models import Posts

class Like(models.Model):
    """
    Like model, related to 'owner' and 'post'.
    'owner' is a User instance and 'post' is a Post instance.
    'unique_together' makes sure a user can't like the same post twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE,
                              related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Ensure uniqueness of the combination of 'owner' and 'posts', i.e.
        # a user cannot like the same post more than once:
        # Effect:
        # This constraint prevents a user from liking the same post more than
        # once. If a user has already liked a particular post, attempting to
        # create another Like instance with the same combination of owner and
        # posts will result in a database integrity error.
        # Enforcement:
        # Django automatically enforces this uniqueness constraint at the
        # database level. If you attempt to create a Like instance that violates
        # this constraint, Django will raise a django.db.IntegrityError.
        # Use Case:
        # This is useful in scenarios where you want to ensure a unique
        # combination of certain fields to maintain data integrity, such as
        # preventing duplicate likes for the same post by the same user.
        # In summary, unique_together helps to define a composite unique
        # constraint on multiple fields in a Django model.
        unique_together = ['owner', 'posts']

    def __str__(self):
        return f'{self.owner} {self.posts}'

