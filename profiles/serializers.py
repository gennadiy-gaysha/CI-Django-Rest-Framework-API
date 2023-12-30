from rest_framework import serializers
from .models import Profile
from followers.models import Follower


# inherits  from ModelSerializer:
class ProfileSerializer(serializers.ModelSerializer):
    # In the context of the original explanation about overwriting the default
    # behavior to display the username for better readability in serialized
    # data, the adjustment is made in the serializer, not in the model.
    # The serializer ensures that when you serialize a Profile instance,
    # the owner field returns the username of the associated User rather than
    # the default id.
    owner = serializers.ReadOnlyField(source='owner.username')
    # 1) is_owner Field:
    # is_owner is a custom field that we're adding to the ProfileSerializer.
    # Unlike fields such as CharField or IntegerField, SerializerMethodField
    # allows you to define a custom method to determine the value of the field.
    # 2) SerializerMethodField:
    # SerializerMethodField is a field provided by Django REST framework that
    # allows us to define a custom method to determine the value of the field.
    # It doesn't directly map to a model field but gives you flexibility to
    # include custom logic when serializing data.
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()

    # This method takes two parameters:
    # self: The instance of the serializer.
    # obj: The object being serialized (in this case, a Profile instance).
    # get_is_owner method uses the request object from the context to check if
    # the user making the request is the owner of the profile being serialized.
    # This helps in determining whether the user has ownership permissions based
    # on the custom logic defined in get_is_owner.
    def get_is_owner(self, obj):
        # self.context is a dictionary that provides additional context to the
        # serializer. In this case, it includes the request object.
        # request = self.context['request'] retrieves the request object from
        # the context.
        request = self.context['request']
        # request.user represents the user making the request (sets request.user
        # attribute to the corresponding user object if the user is authenticated)
        # obj.owner represents the owner of the profile being serialized.
        return request.user == obj.owner

    def get_following_id(self, obj):
        # This line retrieves the user making the request from the context. The
        # self.context['request'] represents the request object, and user will
        # contain the user associated with the request.
        user = self.context['request'].user
        print(user)
        if user.is_authenticated:
            # This line queries the Follower model to check if the requesting
            # user (owner=user) is following the owner of the profile being
            # serialized (followed=obj.owner). The first() method retrieves the
            # first matching record or returns None if no match is found.

            # owner - This refers to the field in the Follower model that
            # represents the user who is following someone. In the line
            # owner=user means that it's looking for instances where the owner
            # field in the Follower model is equal to the currently logged-in
            # user (user).

            # user - This is the currently logged-in user, retrieved from the
            # request context.

            # following - This variable holds the result of the query, and in
            # this context, it's an instance of the Follower model (if a match
            # is found) or None (if no match is found).
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            # __str__ method is responsible for defining the string representation
            # of instances of the Follower model. When you use print(following),
            # Python calls the __str__ method to convert the object to a string.
            print(following)
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'email', 'name',
            'content', 'image', 'is_owner', 'following_id',
        ]

# This is a Django REST Framework (DRF) serializer class named `ProfileSerializer`.
# Serializers in DRF define how to convert complex data types, such as Django
# models, into Python Native Data Types that can be easily rendered into JSON
# or other content types. They also handle the reverse process of deserialization,
# converting incoming data into Python objects.
# Let's break down the elements of the provided `ProfileSerializer` class:
#
# 1. **Owner Field:**
#    ```python
#    owner = serializers.ReadOnlyField(source='owner.username')
#    ```
#    - This line creates a field named `owner` in the serializer.
#    - It uses `serializers.ReadOnlyField` to indicate that this field is read-only
#    and should not be used for deserialization (i.e., when receiving data in a POST
#    or PUT request).
#    - The `source='owner.username'` attribute specifies that the data for this
#    field should be obtained from the `username` attribute of the `owner` attribute
#    of the `Profile` model.
#
# 2. **Meta Class:**
#    ```python
#    class Meta:
#        model = Profile
#        fields = [
#            'id', 'owner', 'email', 'created_at', 'updated_at', 'name',
#            'content', 'image'
#        ]
#    ```
#    - The `Meta` class is used to provide additional information about the serializer.
#    - `model = Profile` specifies that this serializer is associated with the `Profile`
#    model.
#    - `fields` is a list of fields to include in the serialized representation of the
#    `Profile` model. In this case, it includes various fields such as `id`, `owner`,
#    `email`, etc.
#
# In summary, this serializer is designed to serialize instances of the `Profile`
# model into a JSON representation. It includes read-only information about the
# owner of the profile (specifically, the owner's username) in the serialized data.
# The serializer is tailored to include specific fields from the `Profile` model
# in the output. The `ReadOnlyField` ensures that the `owner` field is not used
# for deserialization.
