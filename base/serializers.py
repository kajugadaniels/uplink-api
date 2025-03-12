from base.models import *
from mobile.serializers import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    
    Serializes the 'name' field provided by the user and the auto-generated 'slug' field,
    and includes a nested list of posts associated with the category.
    """
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'posts']
        read_only_fields = ['slug']
