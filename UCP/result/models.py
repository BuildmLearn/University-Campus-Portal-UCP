"""
Models file for Result App

consists of the model definitions for the result app
"""

from django.utils import timezone
from django.db import models
from login.models import UserProfile
from discussion.models import Tag
from UCP.functions import get_time_elapsed_string, get_file_size_string

# Create your models here.

class Result(models.Model):
    """
    Stores a Result, related to :class:`login.models.UserProfile` and
    :class:`discussion.models.Tag`
    """
    teacher = models.ForeignKey(UserProfile)
    result_file = models.FileField(upload_to="result_files")
    title = models.CharField(blank=True, max_length=100)
    tags = models.ManyToManyField(Tag)
    posted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-posted_at']
    
    def time_elapsed(self):
        return get_time_elapsed_string(self.posted_at)
        
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title
