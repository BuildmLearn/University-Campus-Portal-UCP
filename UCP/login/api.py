from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render
from django.template import Context
from django.utils import timezone
from django.views.generic import View

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

from login.models import EmailVerificationCode, PasswordResetCode
from login.functions import login, register, forgot_password, reset_password, verify_email
import login.serializers as Serializers
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL


class UserViewSet(viewsets.ViewSet):
    """
    Viewset for registering and logging in users
    """
    
    @list_route()
    def login(self, request):
        """
        email -- User's email
        password -- User's password
        """
        
        response = login(request)
            
        return Response(response, status=status.HTTP_200_OK)
        
    @list_route(methods=['post'])
    def register(self, request, format=None):
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
    
    @list_route()
    def verify_email(self, request, format=None):
        """
        code -- code for email verification
        """
        
        response = verify_email(request)
        
        return Response(response, status=status.HTTP_200_OK)

class UserPasswordViewSet(viewsets.ViewSet):
    """
    Viewsets for password related apis
    """
    
    @list_route()
    def forgot_password(self, request):
        """
        email -- Email of the user
        """
        response = forgot_password(request)
            
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])
    def reset_password(self, request):
        """
        ---
        request_serializer: Serializers.PasswordResetRequestSerializer
        """
        
        response = reset_password(request)
            
        return Response(response, status=status.HTTP_200_OK)