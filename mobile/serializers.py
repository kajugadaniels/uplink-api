from base.models import *
from mobile.models import *
from account.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to represent detailed user information.
    Exposes the user's name, email, phone number, username, and image.
    """
    class Meta:
        model = User
        fields = ('name', 'email', 'phone_number', 'username', 'image')

class PostImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the PostImage model.
    
    Overrides the default image field serialization to return the absolute URL of the image.
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = PostImage
        fields = ('id', 'image', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_image(self, obj):
        """
        Returns the absolute URL of the image using the request context.
        """
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class PostLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the PostLike model.
    
    - The 'user' field is represented using the detailed UserSerializer and is read-only.
    - The 'post' field accepts a primary key.
    - During creation, the logged-in user is automatically assigned.
    """
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = PostLike
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('id', 'created_at', 'user')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

class PostCommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the PostComment model.

    - Represents detailed user information via a nested UserSerializer.
    - Accepts a post primary key for input.
    - Automatically assigns the logged-in user on creation.
    """
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = PostComment
        fields = ('id', 'user', 'post', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)