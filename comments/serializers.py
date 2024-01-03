from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
        Serializer for the Comment model
        Adds three extra fields when returning a list of Comment instances
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_is_owner(self, obj):
        '''
        This method takes two parameters: self (the instance of the serializer)
        and obj (the comment object being serialized).
        It retrieves the request object from the serializer's context. The
        context usually includes information about the request being processed.
        It then compares the user making the request (request.user) with the
        owner of the comment (obj.owner).
        If the current user is the owner of the comment, the method returns
        True; otherwise, it returns False.
        '''
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'posts', 'created_at', 'updated_at', 'content'
        ]

class CommentDetailSerializer(CommentSerializer):
    posts = serializers.ReadOnlyField(source='posts.id')
