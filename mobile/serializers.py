from mobile.models import *
from rest_framework import serializers

class PostImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the PostImage model.
    
    Handles serialization for a post image, exposing the image field and its creation timestamp.
    """
    class Meta:
        model = PostImage
        fields = ('id', 'image', 'created_at')
        read_only_fields = ('id', 'created_at')