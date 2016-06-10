from django.db import models

from login.models import UserProfile


class Tag(models.Model):
    
    name = models.CharField(null=True, max_length=100)
    
    def __unicode__(self):
        return self.name


class DiscussionThread(models.Model):
    
    title = models.CharField( max_length=100)
    description = models.CharField( max_length=1000)
    posted_by = models.ForeignKey(UserProfile, null=True)
    posted_at = models.DateField(null=True)
    no_of_replies = models.IntegerField(blank=True, null=True, default=0)
    no_of_views = models.IntegerField(blank=True, null=True, default=0)
    last_reply = models.ForeignKey("Reply", related_name="last_reply", null=True, blank=True)
    tag = models.ForeignKey(Tag,null=True)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title


class Reply(models.Model):
    
    thread = models.ForeignKey(DiscussionThread)
    posted_by = models.ForeignKey(UserProfile, null=True)
    posted_at = models.DateField(null=True)
    text = models.CharField(null=True, max_length="1000")
    
    def __unicode__(self):
        return self.text[:20]


class Attachment(models.Model):
    
    reply = models.ForeignKey(Reply)
    uploaded_file = models.FileField(upload_to="user-attachments")
    size = models.FloatField(null=True, blank=True)
    
    
    
