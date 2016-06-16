from rest_framework import serializers

from discussion.models import DiscussionThread, Tag, Attachment, Reply


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name')


class AttachmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attachment
        fields = ('id', 'uploaded_file', 'size')


class ReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reply
        fields = ('id', 'text', 'posted_at')


class DiscussionThreadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DiscussionThread
        fields = ('id', 'title', 'description', 'no_of_replies', 'no_of_views', 'posted_at')


