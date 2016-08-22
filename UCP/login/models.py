"""
Models file for Login App

consists of the model definitions for the login app
"""

from datetime import timedelta
import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from UCP.settings import VERIFICATION_EMAIL_EXPIRY_TIME,PASSWORD_RESET_CODE_EXPIRY_TIME


class UserProfile(models.Model):
    """
    Teachers and student profiles who are portal users.
    related to :class:`django.contrib.auth.User`
    """
    
    TEACHER = 'Teacher'
    STUDENT = 'Student'

    MALE = "male"
    FEMALE = "female"
    


    DESIGNATION_CHOICES =(
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student')
    )

    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female')
    )
    

    user = models.OneToOneField(User, unique=True, related_name='user_login')
    is_moderator = models.BooleanField(default=True)
    designation = models.CharField( choices = DESIGNATION_CHOICES, default=STUDENT, max_length=10)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices = GENDER_CHOICES, default=MALE, max_length=6)
    profile_image = models.ImageField(upload_to="user_images/profile_images", blank=True)
    followed_tags = models.ManyToManyField("discussion.Tag", null=True)
    
    class Admin:
        list_display = ('first_name','designation')
        search_fields = ('first_name','last_name','designation')

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


class EmailVerificationCode(models.Model):
    """
    Codes for verifying user emails after registration
    related to :class:`django.contrib.auth.User`
    """
    
    user = models.ForeignKey(User)
    verification_code = models.CharField(blank=True, max_length=100)
    expiry_date = models.DateField()
    
    def set_expiry_date(self):
        """
        Set the expiry date for code to 30 days from the time now
        """
        return timezone.now()+timedelta(days=VERIFICATION_EMAIL_EXPIRY_TIME)
        
    def create_hash_code(self):
        """
        Create a random hash code
        """
        return os.urandom(32).encode('hex')
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = self.set_expiry_date()
            self.verification_code = self.create_hash_code()
        super(EmailVerificationCode, self).save(*args, **kwargs)


class PasswordResetCode(models.Model):
    """
    Codes for users to recover their accounts
    related to :class:`django.contrib.auth.User`
    """
    
    user = models.ForeignKey(User)
    reset_code = models.CharField(blank=True, max_length=100)
    expiry_date = models.DateField()
    
    def set_expiry_date(self):
        """
        Set the expiry date for code to 30 days from the time now
        """
        return timezone.now()+timedelta(days=PASSWORD_RESET_CODE_EXPIRY_TIME)
        
    def create_hash_code(self):
        """
        Create a random hash code
        """
        return os.urandom(6).encode('hex')
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = self.set_expiry_date()
            self.reset_code = self.create_hash_code()
        super(PasswordResetCode, self).save(*args, **kwargs)


