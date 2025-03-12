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

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    
    Serializes the 'name' field provided by the user and the auto-generated 'slug' field.
    Also includes a nested list of posts (using PostSerializer) associated with the category.
    """
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'posts']
        read_only_fields = ['slug']

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

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model including nested user, category, images, likes, and comments.
    
    Accepts 'category_id' as a write-only field for input and outputs detailed category data via 'category'.
    """
    user = UserSerializer(read_only=True)
    # Write-only field for input: now directly uses Category model to avoid circular dependency
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    # Read-only nested representation for output
    category = CategorySerializer(read_only=True)
    images = PostImageSerializer(many=True, required=False)
    likes = PostLikeSerializer(many=True, read_only=True)
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'category_id', 'category', 'description',
                  'created_at', 'updated_at', 'images', 'likes', 'comments')
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