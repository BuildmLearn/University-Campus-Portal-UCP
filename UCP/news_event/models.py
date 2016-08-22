"""
Models file for News and Event App

consists of the model definitions for the news_event app
"""

from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from discussion.models import Tag
from login.models import UserProfile
from UCP.functions import get_time_elapsed_string, get_file_size_string


class EventQueryset(models.query.QuerySet):
    
    def approved(self):
        return self.filter(is_approved = True)
    
    def pending(self):
        return self.filter(is_approved = False, is_rejected = False)


class EventManager(models.Manager):
    
    def get_queryset(self):
        return EventQueryset(self.model, using=self._db)
    
    def approved(self):
        return self.get_queryset().approved()
        
    def pending(self):
        return self.get_queryset().pending()
        
        
# Create your models here.
class News(models.Model):
    """
    Stores a News article, related to :class:`discussion.models.Tag`
    """
    title = models.CharField(blank=True, max_length=100)
    description = HTMLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    posted_at = models.DateTimeField(blank=True, default=timezone.now)
    posted_by = models.ForeignKey(UserProfile,null =True)
        
    class Meta:
        ordering = ['-posted_at']
        
    def time_elapsed(self):
        """
        returns time elapsed since the news article was posted
        """
        return get_time_elapsed_string(self.posted_at)
        
    def short_description(self):
        """
        returns first 200 characters of the description
        """
        return self.description[:200]+ "..."
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title


class Event(models.Model):
    """
    Stores a Schedule, related to :class:`login.models.UserProfile` and
    :class:`discussion.models.Tag`
    """
    
    title = models.CharField(blank=True, max_length=100)
    description = HTMLField(blank=True, null=True)
    image = models.ImageField(upload_to="event_images",null=True)
    tags = models.ManyToManyField(Tag)
    venue = models.CharField(blank=True, max_length=100)
    event_date = models.DateTimeField(default=timezone.now)
    posted_at = models.DateTimeField(blank=True, default=timezone.now)
    posted_by = models.ForeignKey(UserProfile,null =True)
    is_approved = models.BooleanField(default = False)
    is_rejected = models.BooleanField(default = False)
        
    objects = EventManager()
    
    class Meta:
        ordering = ['-posted_at']
        
    def time_elapsed(self):
        """
        returns time elapsed since the event was posted
        """
        return get_time_elapsed_string(self.posted_at)
        
    def short_description(self):
        """
        returns first 200 characters of the description
        """
        return self.description[:200]+ "..."
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title