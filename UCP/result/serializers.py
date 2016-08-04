from django.contrib.auth.models import User

from rest_framework import serializers

from login.serializers import UserProfileSerializer
from discussion.serializers import TagSerializer
from result.models import Result


class ResultSerializer(serializers.ModelSerializer):
    
    teacher = UserProfileSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Result
        fields = ('id', 'title', 'teacher','tags', 'result_file')
        

class ResultCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Result
        fields = ('id', 'title', 'teacher', 'result_file')
        
    def validate_tags(self, validated_data):
        return validated_data