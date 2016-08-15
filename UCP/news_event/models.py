from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from discussion.models import Tag
from login.models import UserProfile
from UCP.functions import get_time_elapsed_string, get_file_size_string


# Create your models here.
class News(models.Model):
    """(News description)"""
    title = models.CharField(blank=True, max_length=100)
    description = HTMLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    posted_at = models.DateTimeField(blank=True, default=timezone.now)
    posted_by = models.ForeignKey(UserProfile,null =True)
        
    class Meta:
        ordering = ['-posted_at']
        
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
        
    def short_description(self):
        return self.description[:200]+ "..."
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title


class Event(models.Model):
    """(Event description)"""
    
    title = models.CharField(blank=True, max_length=100)
    description = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to="event_images",null=True)
    tags = models.ManyToManyField(Tag)
    venue = models.CharField(blank=True, max_length=100)
    event_date = models.DateTimeField(default=timezone.now)
    posted_at = models.DateTimeField(blank=True, default=timezone.now)
    posted_by = models.ForeignKey(UserProfile,null =True)
    is_approved = models.BooleanField(default = False)
        
    class Meta:
        ordering = ['-posted_at']
        
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
        
    def short_description(self):
        return self.description[:200]+ "..."
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title