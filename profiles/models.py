from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# This model is designed to extend the built-in User model with additional
# profile information, such as a name, content, and an image.
class Profile(models.Model):
    # By default, a OneToOneField creates a database column that stores the
    # primary key (id) of the associated model (User in this case). So, the
    # owner field would initially store the id of the associated User. This
    # is the default behavior when no specific related_name or
    # related_query_name is provided (see serializers.py)...

    # !!! Foreign key field of the model instance is the object of primary key:
    # user_object = profile_instance.owner
    # username = user_object.username
    # user_instance.username = profile_instance.owner.username
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',
                              default='../default_profile_h0pgqr')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


# create_profile function is defined before we pass it as an argument. Because
# we are passing this function to the post_save.connect method, it requires the
# following arguments:
# the sender model, its instance, created - which is a boolean value of whether
# the instance has just been created, and  kwargs.
# Now every time a user is  created, a signal will trigger the Profile model
# to be created.
def create_profile(sender, instance, created, **kwargs):
    # Inside the create_profile function, if created is True
    if created:
        # profile is created whose owner is going to be that user:
        Profile.objects.create(owner=instance, email=instance.email)


# listen for the post_save signal coming  from the User model by calling
# the connect function
# ‘create_profile’ function runs every time the signal is coming
# here we specify User as the model we’re expecting to receive the signal
# from (when new instance of the User is created)
post_save.connect(create_profile, sender=User)
