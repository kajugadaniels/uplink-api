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