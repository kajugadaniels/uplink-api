from base.models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Serializes the 'name' field provided by the user and the auto-generated 'slug' field.
    """
    class Meta:
        model = Category
        fields = ['name', 'slug']
        read_only_fields = ['slug']
