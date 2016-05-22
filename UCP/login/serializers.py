from rest_framework import serializers
from django.contrib.auth.models import User
from login.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'designation', 'profile_image')
        read_only_fields = ('id',)
