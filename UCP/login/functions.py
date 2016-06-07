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


def login(request):
    
    serializer = Serializers.LoginRequestSerializer(data = request.GET)
    if serializer.is_valid(): 
        
        username = request.GET['email']
        password = request.GET['password']
    
        user = authenticate(username=username, password=password)
        
        response = {}
        
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
    
    return response
    
def register(request):
    
    response = {}
    
    serializer = Serializers.UserSerializer(data=request.POST)
    
    if serializer.is_valid():
        user = serializer.save()
        userProfileSerializer = Serializers.UserProfileSerializer(data=request.POST)
        if userProfileSerializer.is_valid():
            userProfileSerializer.save(user = user)
            response["result"] = result.RESULT_SUCCESS
            response["message"]= message.MESSAGE_REGISTRATION_SUCCESSFUL 
            response["error"] = []
            #send a verification email
            #sendVerificationEmail(user)
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = message.MESSAGE_REGISTRATION_FAILED
            response["error"] = userProfileSerializer.errors
    else:
        response["result"] = result.RESULT_FAILURE
        response["message"] = message.MESSAGE_REGISTRATION_FAILED
        response["error"] = serializer.errors
    
    return response
    