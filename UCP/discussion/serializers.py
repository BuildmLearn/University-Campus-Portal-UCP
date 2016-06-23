from django.contrib.auth.models import User

from rest_framework import serializers

from login.models import UserProfile
from discussion.models import DiscussionThread, Tag, Attachment, Reply


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class UserProfileShortSerializer(serializers.ModelSerializer):
    
    user = UserShortSerializer()
    class Meta:
        model = UserProfile
        fields = ('id', 'designation', 'user', 'profile_image')


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name')


class AttachmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attachment
        fields = ('id', 'uploaded_file', 'size_in_kb', 'name')


class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = ('id', 'text', 'posted_at', 'time_elapsed')


class ReplyFullSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    posted_by = UserProfileShortSerializer()
    
    class Meta:
        model = Reply
        fields = ('id', 'text', 'posted_at', 'time_elapsed', 'posted_by', 'attachments')

class DiscussionThreadSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = DiscussionThread
        fields = ('id', 'title', 'description', 'no_of_replies', 'no_of_views', 'posted_at', 'time_elapsed')


class DiscussionThreadFullSerializer(serializers.ModelSerializer):
    posted_by = UserProfileShortSerializer()
    
    class Meta:
        model = DiscussionThread
        fields = ('id', 'title', 'description', 'no_of_replies', 'no_of_views', 'posted_at', 
        'posted_by', 'time_elapsed')
