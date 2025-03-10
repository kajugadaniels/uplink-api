import random
from account.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Override the validate method to authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')

        # Check if the email is provided
        if not email:
            raise ValidationError("Email is required.")

        # Check if the password is provided
        if not password:
            raise ValidationError("Password is required.")

        # Attempt to fetch the user from the database
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("No user found with this email address.")

        # Check if the password is correct
        if not user.check_password(password):
            raise ValidationError("Incorrect password. Please check your credentials.")

        # Generate JWT tokens for successful login
        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)

        return attrs

class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'name', 
            'email', 
            'username', 
            'phone_number', 
            'image', 
            'password', 
            'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists. Please use a different email address."
            )
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A user with this phone number already exists. Please use a different phone number."
            )
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(
                {"password": "Password and confirm password do not match. Please re-enter them."}
            )
        return attrs

    def create(self, validated_data):
        # Remove confirm_password as it is not needed for user creation.
        validated_data.pop('confirm_password')
        username = validated_data.get('username')
        
        # If a username is provided, ensure it's unique by appending 4 random digits if necessary.
        if username:
            base_username = username
            # Loop until a unique username is found.
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{random.randint(1000, 9999)}"
            validated_data['username'] = username

        # Use the custom user manager to handle user creation (including password hashing).
        user = User.objects.create_user(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=validated_data.get('username'),
            phone_number=validated_data.get('phone_number'),
            image=validated_data.get('image'),
            password=validated_data.get('password')
        )
        return user