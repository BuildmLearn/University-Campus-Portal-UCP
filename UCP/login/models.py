from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Teachers and student profiles who are portal users.
    """
    DESIGNATION_CHOICES =(
        (0, 'Teacher'),
        (1, 'Student')
    )
    
    user = models.OneToOneField(User)
    first_name = models.CharField(null=True, max_length=100)
    last_name = models.CharField(null=True, max_length=100)
    designation = models.IntegerField(blank=True, choices = DESIGNATION_CHOICES, default=0, null=True)
    profile_image = models.ImageField(upload_to="/user_images/profile_images")

    class Admin:
        list_display = ('first_name','designation')
        search_fields = ('first_name','last_name','designation')

    def __unicode__(self):
        return first_name + " " + last_name
