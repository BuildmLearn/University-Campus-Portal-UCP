"""
Seriliazers file for Login App

contains serializers for models of the login app, as well as request serializers that are used to check if a request 
is valid.
"""

from django.contrib.auth.models import User

from rest_framework import serializers

from login.models import UserProfile
from UCP.constants import error

#MODEL SERIALIZERS

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new django.contrib.auth.models.User object
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'].capitalize(),
            last_name=validated_data['last_name'].capitalize()
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
    
    def validate_email(self, value):
        """
        Checks if a user with this email already exists
        """
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(error.ERROR_VALIDATION_EMAIL_EXISTS)
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new User Profile object
    """
    class Meta:
        model = UserProfile
        fields = ('id','designation', 'profile_image')
        read_only_fields = ('id',)


class UserProfileFullSerializer(serializers.ModelSerializer):
    """
    Serializer for getting full details of a User Profile object
    """
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('id','designation', 'profile_image', 'user', 'age', 'gender', 'is_moderator', 'followed_tags')
        read_only_fields = ('id',)


class UserShortSerializer(serializers.ModelSerializer):
    """
    Serializer for getting limited details of a django.contrib.auth.models.User object
    """
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class UserProfileShortSerializer(serializers.ModelSerializer):
    """
    Serializer for getting limited details of a UserProfile Object
    """
    user = UserShortSerializer()
    class Meta:
        model = UserProfile
        fields = ('id', 'designation', 'user', 'profile_image')


#REQUEST SERIALIZERS
class LoginRequestSerializer(serializers.Serializer):
    """
    Serializer for verifying if the request by the login API is valid
    """
    
    email = serializers.EmailField()
    password = serializers.CharField()
    

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for verifying if the request by the Reset password API is valid
    """
    
    reset_code = serializers.CharField()
    password = serializers.CharField()
    

class PasswordForgotRequestSerializer(serializers.Serializer):
    """
    Serializer for verifying if the request by the Forgot password API is valid
    """
    
    email = serializers.EmailField()
    
    
class VerifyEmailRequestSerializer(serializers.Serializer):
    """
    Serializer for verifying if the request by the verify email API is valid
    """
    
    code = serializers.CharField()
    
    