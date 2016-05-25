from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import render

from login.serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from UCP.constants import result, message
from login.models import EmailVerificationCode, PasswordResetCode
from UCP.settings import EMAIL_HOST_USER
# Create your views here.

def sendVerificationEmail(user):
    """
    Creates a EmailVerificationCode Object and send a verification mail to the user
    """
    emailVerificationCode = EmailVerificationCode.objects.create(user=user)
    emailSubject = "Verification Email"
    emailMessage = "localhost:8000/user-auth/verify_email/?email=" + user.email+"&code="+ emailVerificationCode.verification_code+"&format=json"
    to = [user.email]
    senderEmail = EMAIL_HOST_USER
    print emailMessage
    #send_mail(emailSubject, emailMessage, senderEmail, to, fail_silently=False)


def sendPasswordResetEmail(user):
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


    
class UserRegistration(APIView):
    '''
    Creates a new user profile
    '''
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            user = serializer.save()
            userProfileSerializer = UserProfileSerializer(data=request.data)
            if userProfileSerializer.is_valid():
                userProfileSerializer.save(user = user)
                response["result"] = result.RESULT_SUCCESS
                response["data"] = userProfileSerializer.data
                #send a verification email
                sendVerificationEmail(user)
                return Response(response, status=status.HTTP_201_CREATED)
        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    '''
    Handles Login API
    '''
    def post(self, request, format=None):
        response = {}
        
        username = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                response["result"] = result.RESULT_SUCCESS
                response["message"] = message.MESSAGE_LOGIN_SUCCESSFUL
            else:
                response["result"] = result.RESULT_FAILURE
                response["message"] = message.MESSAGE_ACCOUNT_INACTIVE
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = message.MESSAGE_INVALID_LOGIN_DETAILS
        return Response(response, status=status.HTTP_200_OK)
        
class VerifyEmail(APIView):
    """
    Verify user email from the link sent to their email 
    """
    def get(self, request, format=None):
        response = {}
        
        email = request.GET['email']
        verification_code = request.GET['code']
        
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email=email)
            if EmailVerificationCode.objects.filter(verification_code = verification_code,user=user).exists():
                #verify the user
                user.is_active = True
                user.save()
                response["result"] = result.RESULT_SUCCESS
                response["message"] = "User email is successfully verified"
            else:
                response["result"] = result.RESULT_FAILURE
                response["message"] = "The verification code provided does not exist or might have been expired"
                #invalid or expired verification code
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = "Given email Id is not registered"
            #invalid email provided
            
        return Response(response, status=status.HTTP_200_OK)
        
class ForgotPassword(APIView):
    """
    Sends a password reset link to the user
    """
    def get(self, request, format=None):
        response = {}
        
        email = request.GET['email']
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email=email)
            sendPasswordResetEmail(user)
            response["result"] = result.RESULT_SUCCESS
            response["message"] = "Instructions to reset your password have been sent to your email id"
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = "Given email Id is not registered"
            #invalid email provided
            
        return Response(response, status=status.HTTP_200_OK)
        
        
class ResetPassword(APIView):
    """
    Resets a user's password using a password reset code
    """
    def post(self, request, format=None):
        response = {}
        reset_code = request.POST['reset_code']
        password = request.POST['password']
        
        if PasswordResetCode.objects.filter(reset_code = reset_code).exists():
            user = PasswordResetCode.objects.get(reset_code = reset_code).user
            user.set_password(password)
            user.save()
            response["result"] = result.RESULT_SUCCESS
            response["message"] = "Your password has been reset"
        else:
            response["result"] = result.RESULT_FAILURE
            response["message"] = "The password code is not valid"
        
        return Response(response, status=status.HTTP_200_OK)

