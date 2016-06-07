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
from login.functions import login, register, forgot_password, reset_password, verify_email
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL
# Create your views here.

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
        response = register(request)
        
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
        
        response = login(request)
            
        return Response(response, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    """
    Verify user email from the link sent to their email 
    """
    
    def get(self, request, format=None):
        """
        code -- code for email verification
        """
        
        response = verify_email(request)
        
        return Response(response, status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    """
    Sends a password reset link to the user
    """
    
    def get(self, request, format=None):
        """
        email -- Email of the user
        """
        response = forgot_password(request)
            
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
        
        response = reset_password(request)
            
        return Response(response, status=status.HTTP_200_OK)


