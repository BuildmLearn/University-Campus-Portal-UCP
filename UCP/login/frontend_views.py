from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import Context
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
from login.functions import login, register, forgot_password, reset_password

from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL


class Login(View):
    
    def get(self, request):
        context = {}
        context["is_login_page"] = True
        
        if not 'email' in request.GET:
            return render(request, 'login-register.html', context)
        
        response = login(request)
        
            
        context["response"] = response
        return render(request, 'login-register.html', context)


class Register(View):
    
    def get(self, request):
        return render(request, 'login-register.html')
        
    def post(self, request):

        context={}
        
        response = register(request)
        
        errors = []
        
        for key in response["error"]:
            for error in response["error"][key]:
                errors.append(error)
        
        response["errors"] = errors
        context["response"] = response
        
        print response
        return render(request, 'login-register.html', context)
        

class ForgotPassword(View):
    
    def get(self, request):
        
        context={}
        response = forgot_password(request)
        context["response"] = response
        
        if(response["result"] == 0):
            return render(request, 'login-register.html', context)
        if(response["result"] == 1):
            return render(request, 'reset-password.html', context)
       
        
class ResetPassword(View):
    
    def post(self, request):
        
        context={}
        response = reset_password(request)
        context["response"] = response
        
        
        if(response["result"] == 1):
            return render(request, 'login-register.html', context)
        if(response["result"] == 0):
            return render(request, 'reset-password.html', context)
        
        
        
        
