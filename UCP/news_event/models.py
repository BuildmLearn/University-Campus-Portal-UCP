from django.db import models
from django.utils import timezone

from discussion.models import Tag

# Create your models here.
class News(models.Model):
    """(News description)"""
    title = models.CharField(blank=True, max_length=100)
    description = models.CharField(blank=True, max_length=10000)
    tags = models.ManyToManyField(Tag)
    date = models.DateTimeField(blank=True, default=timezone.now)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"News"
