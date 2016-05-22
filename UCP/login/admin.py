from django.contrib import admin
from django.contrib.auth.models import User
from login.models import UserProfile

# Register your models here.

admin.site.register(UserProfile)