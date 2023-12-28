from django.db import IntegrityError
from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    # The purpose of this serializer field is to include the username of the
    # owner (a User instance) in the serialized representation of a Like object.
    # Since it's a read-only field, it's used for serialization (output), but
    # it won't be used for deserialization (input) when creating or updating
    # instances.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'posts']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
