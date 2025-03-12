from base.models import *
from mobile.serializers import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    
    Serializes the 'name' and auto-generated 'slug' fields.
    Also includes a nested list of posts (using PostSerializer) associated with the category.
    """
    posts = PostSerializer(many=True, read_only=True, context={'request': None})

    class Meta:
        model = Category
        fields = ['name', 'slug', 'posts']
        read_only_fields = ['slug']