from mobile.models import *
from account.models import *
from rest_framework import serializers

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

    def update(self, instance, validated_data):
        """
        Update an existing Post instance. If new post images data is provided,
        delete all existing images and create new PostImage instances.
        """
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data is not None:
            # Delete all existing images before adding new ones
            instance.images.all().delete()
            for image_data in images_data:
                PostImage.objects.create(post=instance, **image_data)
        return instance