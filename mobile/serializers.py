from mobile.models import *
from account.models import *
from base.serializers import *
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

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model including nested user, category, and images.
    Accepts 'category_id' as a write-only field for input, while the output 'category' field provides detailed data.
    """
    user = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=CategorySerializer.Meta.model.objects.all() if hasattr(CategorySerializer.Meta, 'model') else None,
        source='category',
        write_only=True
    )
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'category', 'description', 'created_at', 'updated_at', 'images')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        """
        Create a new Post instance along with any associated PostImage instances.
        The logged-in user is automatically assigned as the post's creator.
        """
        images_data = validated_data.pop('images', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            PostImage.objects.create(post=post, **image_data)
        return post

    def update(self, instance, validated_data):
        """
        Update an existing Post instance. If new post images data is provided,
        existing images are deleted and new PostImage instances are created.
        """
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                PostImage.objects.create(post=instance, **image_data)
        return instance