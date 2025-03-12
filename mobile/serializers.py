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