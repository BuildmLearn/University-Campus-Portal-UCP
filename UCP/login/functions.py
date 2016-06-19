"""
Functions file for login app

consists of common functions used by both api.py and views.py file
"""
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
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

from login.models import EmailVerificationCode, PasswordResetCode, UserProfile
import login.serializers as Serializers
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL


def get_user_details(request):
    """
    returns a dict with the details of the logged in user
    """
    user = UserProfile.objects.get(user=request.user)
    serializer = Serializers.UserProfileFullSerializer(user)
    
    return serializer.data

def update_profile(request):
    """
    updates user profile details
    """
    
    user = UserProfile.objects.get(user=request.user)
    
    if "first_name" in request.POST:
        user.user.first_name = request.POST["first_name"]
    if "last_name" in request.POST:
        user.user.last_name = request.POST["last_name"]
    if "profile_picture" in request.FILES:
        user.profile_image = request.FILES["profile_picture"]
        
    user.user.save()
    user.save()
    
    response = {}
    
    response["message"] = "Your details were updated"
    return response

def get_response_text(response):
    messageHTML = ""
    if "message" in response:
        messageHTML += "<h4>" + response["message"] + "</h4>"
        
    if "error" in response:
        for key in response["error"]:
            for error in response["error"][key]:
                messageHTML += "<h4>" + error + "</h4>"
    
    return messageHTML
    
def send_verification_email(user):
    """
    Creates a EmailVerificationCode Object and send a verification mail to the user
    """
    
    emailVerificationCode = EmailVerificationCode.objects.create(user=user)
    emailSubject = "Verification Email"
    emailMessage = "Use the following link to activate your account \n"
    emailMessage += BASE_URL + "/api/user/verify_email/?email=" + user.email+"&code="+ emailVerificationCode.verification_code+"&format=json"
    to = [user.email]
    senderEmail = EMAIL_HOST_USER
    print emailMessage
    #send_mail(emailSubject, emailMessage, senderEmail, to, fail_silently=False)


def send_password_reset_email(user):
    """
    Creates a PasswordResetCode Object and send the code to the user
    """
    
    passwordResetCode = PasswordResetCode.objects.create(user=user)
    emailSubject = "Reset your password"
    emailMessage = "Use the code " + passwordResetCode.reset_code + " to reset your password"
    to = [user.email]
    senderEmail = EMAIL_HOST_USER
    print emailMessage
    #send_mail(emailSubject, emailMessage, senderEmail, to, fail_silently=False)

def login(request):
    
    serializer = Serializers.LoginRequestSerializer(data = request.GET)
    response = {}
    
    if serializer.is_valid(): 
        
        username = request.GET['email']
        password = request.GET['password']
    
        user = authenticate(username=username, password=password)
                
        if user:
            if user.is_active:
                #create a authentication key for the user
                
                django_login(request, user)
                
                data = {}
                if Token.objects.filter(user=user).exists():
                    token = Token.objects.get(user=user)
                else:
                    token = Token.objects.create(user=user)
            
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
            send_verification_email(user)
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = message.MESSAGE_REGISTRATION_FAILED
            response["error"] = userProfileSerializer.errors
    else:
        response["result"] = result.RESULT_FAILURE
        response["message"] = message.MESSAGE_REGISTRATION_FAILED
        response["error"] = serializer.errors
    
    return response
    
def forgot_password(request):
    
    response = {}
    
    serializer = Serializers.PasswordForgotRequestSerializer(data = request.GET)
    if serializer.is_valid():
        email = request.GET['email']
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email=email)
            send_password_reset_email(user)
            response["result"] = result.RESULT_SUCCESS
            response["message"] = message.MESSAGE_PASSWORD_RESET_CODE_SENT
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = message.MESSAGE_EMAIL_NOT_REGISTERED
            #invalid email provided
    else:
        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
    
    return response
    
def reset_password(request):
    
    response = {}
    
    serializer = Serializers.PasswordResetRequestSerializer(data = request.POST)
    if serializer.is_valid():
        reset_code = request.POST['reset_code']
        password = request.POST['password']
    
        if PasswordResetCode.objects.filter(reset_code = reset_code).exists():
            code = PasswordResetCode.objects.get(reset_code = reset_code)
            user = code.user
            user.set_password(password)
            user.save()
        
            #delete the password rest code so it cant be used again
            code.delete()
        
            response["result"] = result.RESULT_SUCCESS
            response["message"] = "Your password has been reset"
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = "The password code is not valid"
    else:
        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response
    
def verify_email(request):
    
    response = {}

    serializer = Serializers.VerifyEmailRequestSerializer(data = request.GET)
    if serializer.is_valid():
    
        verification_code = request.GET['code']
    
        if EmailVerificationCode.objects.filter(verification_code = verification_code).exists():
            #verify the user
            code = EmailVerificationCode.objects.get(verification_code = verification_code)
            user = code.user
            user.is_active = True
            user.save()
        
            #delete verification code so it cant be used again
            code.delete()
        
            response["result"] = result.RESULT_SUCCESS
            response["message"] = message.MESSAGE_EMAIL_VERIFICATION_SUCCESSFUL
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = message.MESSAGE_VERIFICATION_CODE_EXPIRED
            #invalid or expired verification code
    else:
        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response
    
    
