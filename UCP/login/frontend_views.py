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
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL


class Login(View):
    
    def get(self, request):
        context = {}
        context["is_login_page"] = True
        
        if not 'email' in request.GET:
            return render(request, 'login-register.html', context)
        print "this is a form submission request"
        response = {}
        serializer = Serializers.LoginRequestSerializer(data = request.GET)
        if serializer.is_valid(): 
            
            username = request.GET['email']
            password = request.GET['password']
        
            user = authenticate(username=username, password=password)
        
            if user:
                if user.is_active:
                    #create a authentication key for the user
                    token = Token.objects.create(user=user)
                    data = {}
                    data["access_token"] = token.key
                
                    response["result"] = result.RESULT_SUCCESS
                    response["data"] = data
                    response["message"] = message.MESSAGE_LOGIN_SUCCESSFUL
                else:
                    response["result"] = result.RESULT_FAILURE
                    response["message"] = message.MESSAGE_ACCOUNT_INACTIVE
            else:
                response["result"] = result.RESULT_FAILURE
                response["message"] = message.MESSAGE_INVALID_LOGIN_DETAILS
        else:
            response["result"] = result.RESULT_FAILURE
            response["error"] = serializer.errors
            
        context["response"] = response
        return render(request, 'login-register.html', context)


class Register(View):
    
    def get(self, request):
        return render(request, 'login-register.html')
        
    def post(self, request):
        serializer = Serializers.UserSerializer(data=request.POST)
        response = {}
        if serializer.is_valid():
            user = serializer.save()
            userProfileSerializer = Serializers.UserProfileSerializer(data=request.POST)
            if userProfileSerializer.is_valid():
                userProfileSerializer.save(user = user)
                response["result"] = result.RESULT_SUCCESS
                response["message"]= message.MESSAGE_REGISTRATION_SUCCESSFUL 
                #send a verification email
                sendVerificationEmail(user)
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = message.MESSAGE_REGISTRATION_FAILED
            response["error"] = serializer.errors
        
        print response
        return render(request, 'login-register.html')
        
