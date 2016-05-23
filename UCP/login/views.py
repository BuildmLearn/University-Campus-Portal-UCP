from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from login.serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

from UCP.constants import result, message
# Create your views here.
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
        
        username = request.POST['username']
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