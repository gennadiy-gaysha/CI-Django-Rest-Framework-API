from rest_framework import serializers
from .models import Profile


# inherits  from ModelSerializer:
class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = [
            'id', 'owner', 'email', 'created_at', 'updated_at', 'name',
            'content', 'image'
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
