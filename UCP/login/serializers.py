from django.contrib.auth.models import User

from rest_framework import serializers

from login.models import UserProfile
from UCP.constants import error



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
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
    
    class Meta:
        model = UserProfile
        fields = ('id','designation', 'profile_image')
        read_only_fields = ('id',)


