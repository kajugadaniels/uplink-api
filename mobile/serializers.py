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

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    
    This serializer includes a nested representation of associated post images,
    allowing the creation and update of a post along with multiple images.
    """
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'category', 'description', 'created_at', 'updated_at', 'images')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        """
        Create a new Post instance along with any associated PostImage instances if provided.
        """
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            PostImage.objects.create(post=post, **image_data)
        return post