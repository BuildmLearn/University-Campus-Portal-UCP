from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone

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
# Create your views here.

def sendVerificationEmail(user):
    """
    Creates a EmailVerificationCode Object and send a verification mail to the user
    """
    
    emailVerificationCode = EmailVerificationCode.objects.create(user=user)
    emailSubject = "Verification Email"
    emailMessage = "Use the following link to activate your account \n"
    emailMessage += BASE_URL + "/user-auth/verify_email/?email=" + user.email+"&code="+ emailVerificationCode.verification_code+"&format=json"
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
    """
    Creates a new user profile
    """
    
    def post(self, request, format=None):
        """
        ---
        # YAML
        
        parameters:
            - name: email
              description: user email
              required: true
              type: string
              paramType: form
            - name: password
              required: true
              type: string
              paramType: form
            - name: first_name
              required: true
              type: string
              paramType: form
            - name: last_name
              required: true
              type: string
              paramType : form
            - name: designation
              required: true
              paramType: form
              type: string
              description: 0-Teacher 1-Student
        
        """
        serializer = Serializers.UserSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            user = serializer.save()
            userProfileSerializer = Serializers.UserProfileSerializer(data=request.data)
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
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    '''
    Handles Login API
    '''
    serializer_class = Serializers.LoginRequestSerializer
    def get(self, request, format=None):
        """
        email -- User's email
        password -- User's password
        """
        
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
            
        return Response(response, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    """
    Verify user email from the link sent to their email 
    """
    
    def get(self, request, format=None):
        """
        code -- code for email verification
        """
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
            
        return Response(response, status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    """
    Sends a password reset link to the user
    """
    
    def get(self, request, format=None):
        """
        email -- Email of the user
        """
        response = {}
        
        serializer = Serializers.PasswordForgotRequestSerializer(data = request.GET)
        if serializer.is_valid():
            email = request.GET['email']
            if User.objects.filter(email = email).exists():
                user = User.objects.get(email=email)
                sendPasswordResetEmail(user)
                response["result"] = result.RESULT_SUCCESS
                response["message"] = message.MESSAGE_PASSWORD_RESET_CODE_SENT
            else:
                response["result"] = result.RESULT_FAILURE
                response["message"] = message.MESSAGE_EMAIL_NOT_REGISTERED
                #invalid email provided
        else:
            response["result"] = result.RESULT_FAILURE
            response["error"] = serializer.errors
            
        return Response(response, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    """
    Resets a user's password using a password reset code
    """
    
    
    def post(self, request, format=None):
        """
        ---
        request_serializer: Serializers.PasswordResetRequestSerializer
        """
        response = {}
        
        serializer = Serializers.VerifyEmailRequestSerializer(data = request.GET)
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
            
        return Response(response, status=status.HTTP_200_OK)


