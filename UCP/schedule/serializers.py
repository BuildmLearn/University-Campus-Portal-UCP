from django.contrib.auth.models import User

from rest_framework import serializers

from login.serializers import UserProfileSerializer
from discussion.serializers import TagSerializer
from schedule.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    
    teacher = UserProfileSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = Schedule
        fields = ('id', 'title', 'teacher','tags', 'schedule_file')
        

class ScheduleCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Schedule
        fields = ('id', 'title', 'teacher', 'schedule_file')
        