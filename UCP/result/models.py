from django.db import models
from login.models import UserProfile
from discussion.models import Tag
# Create your models here.

class Result(models.Model):
    """(Result description)"""
    teacher = models.ForeignKey(UserProfile)
    result_file = models.FileField(upload_to="result_files")
    title = models.CharField(blank=True, max_length=100)
    tags = models.ManyToManyField(Tag)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return self.title
