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
