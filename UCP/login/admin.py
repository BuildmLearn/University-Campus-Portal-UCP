"""
Admin file for Login App thats takes care of how the models are displayed in the admin panel
"""
from django.contrib import admin
from django.contrib.auth.models import User
from login.models import UserProfile, EmailVerificationCode, PasswordResetCode

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmailVerificationCode)
admin.site.register(PasswordResetCode)