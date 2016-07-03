from django.db import models
from django.utils import timezone

from login.models import UserProfile
from UCP.functions import get_time_elapsed_string, get_file_size_string

class Tag(models.Model):
    
    name = models.CharField(null=True, max_length=100)
    
    def __unicode__(self):
        return self.name


class DiscussionThread(models.Model):
    
    title = models.CharField( max_length=100)
    description = models.CharField( max_length=1000)
    posted_by = models.ForeignKey(UserProfile, null=True, blank=True)
    posted_at = models.DateTimeField(default=timezone.now)
    no_of_replies = models.IntegerField(blank=True, null=True, default=0)
    no_of_views = models.IntegerField(blank=True, null=True, default=0)
    last_reply = models.ForeignKey("Reply", related_name="last_reply", null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    subscribed = models.ManyToManyField(UserProfile, related_name="subscribed")
    
    class Meta:
        ordering = ['-posted_at']
    
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title


class Reply(models.Model):
    
    thread = models.ForeignKey(DiscussionThread)
    posted_by = models.ForeignKey(UserProfile, null=True, blank=True)
    posted_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(default="", max_length="1000")
    
    class Meta:
        ordering = ['-posted_at']
    
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
    


class Attachment(models.Model):
    
    name = models.CharField(blank=True ,null=True, max_length=100)
    reply = models.ForeignKey(Reply, related_name="attachments")
    uploaded_file = models.ImageField(upload_to="user-attachments")
    size = models.FloatField(default=0, blank=True)
    
    def size_in_kb(self):
        return get_file_size_string(self.size)
    
    def save(self, *args, **kwargs):
        self.name = self.uploaded_file.name
        self.size = self.uploaded_file.size
        super(Attachment, self).save(*args, **kwargs)
        
    
    
    
