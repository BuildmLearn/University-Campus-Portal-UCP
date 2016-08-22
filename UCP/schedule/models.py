"""
Models file for Schedule App

consists of the model definitions for the schedule app
"""

from django.utils import timezone
from django.db import models
from login.models import UserProfile
from discussion.models import Tag
from UCP.functions import get_time_elapsed_string, get_file_size_string

# Create your models here.

class Schedule(models.Model):
    """
    Stores a Schedule, related to :class:`login.models.UserProfile` and
    :class:`discussion.models.Tag`
    """
    teacher = models.ForeignKey(UserProfile)
    schedule_file = models.FileField(upload_to="schedule_files")
    title = models.CharField(blank=True, max_length=100)
    tags = models.ManyToManyField(Tag)
    posted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-posted_at']
    
    def time_elapsed(self):
        """
        returns time elapsed since the schedule was posted
        """
        return get_time_elapsed_string(self.posted_at)
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title
