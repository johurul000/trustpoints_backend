from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AppUser
from django.contrib.auth import get_user_model


class AppUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = AppUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'points',
            'password',
            'is_superuser',
            'is_admin'
        ]
        read_only_fields = ['id', 'points', 'is_superuser']  # Users cannot edit these

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = AppUser(**validated_data)
        user.set_password(password)  # Hash password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'points': user.points,  # Include user's reward points
        })
        return data

class SimpleRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=AppUser.objects.all(), message="Email already exists.")]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=AppUser.objects.all(), message="Username already exists.")]
    )
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8)

    class Meta:
        model = AppUser
        fields = ['email', 'username', 'password1', 'password2']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        user = AppUser.objects.create(**validated_data)
        user.set_password(password)  # Hash password
        user.save()
        return user
    


User = get_user_model()

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Get the new access token

        # Extract user ID from the refresh token
        refresh = RefreshToken(attrs["refresh"])
        user_id = refresh.payload.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            data.update({
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            })
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        return data

