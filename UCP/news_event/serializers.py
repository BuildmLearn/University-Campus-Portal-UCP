from django.contrib.auth.models import User

from rest_framework import serializers

from login.models import UserProfile
from discussion.serializers import UserShortSerializer, UserProfileShortSerializer
from news_event.models import Event, News


class EventSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Event
        fields = ('id', 'title', 'description','posted_at', 'image')
        
        
class NewsSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = News
        fields = ('id', 'title', 'description')