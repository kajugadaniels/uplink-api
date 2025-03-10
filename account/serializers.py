from account.models import *
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        help_text="Enter your email, phone number, or username."
    )
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if not identifier:
            raise ValidationError("Identifier (email, phone number, or username) is required.")
        if not password:
            raise ValidationError("Password is required.")

        User = get_user_model()
        try:
            # Query user using email (case-insensitive), phone number, or username (case-insensitive)
            user = User.objects.get(
                Q(email__iexact=identifier) | Q(phone_number=identifier) | Q(username__iexact=identifier)
            )
        except User.DoesNotExist:
            raise ValidationError("No user found with the provided email, phone number, or username.")

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
            raise serializers.ValidationError("A user with this email already exists. Please use a different email address.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists. Please use a different phone number.")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password and confirm password do not match. Please re-enter them."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        # Using the custom manager to create the user ensures the password is hashed properly.
        user = User.objects.create_user(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            username=validated_data.get('username'),
            phone_number=validated_data.get('phone_number'),
            image=validated_data.get('image'),
            password=validated_data.get('password')
        )
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Enter the email address associated with your account."
    )

    def validate_email(self, value):
        User = get_user_model()
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value