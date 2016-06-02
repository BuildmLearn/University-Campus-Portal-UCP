from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from login.models import EmailVerificationCode, PasswordResetCode
import login.serializers as Serializers
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL


class Login(View):
    
    def get(self, request):
        return render(request, 'login-register.html')