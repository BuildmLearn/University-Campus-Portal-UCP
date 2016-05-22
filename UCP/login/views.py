from django.shortcuts import render
from django.contrib.auth.models import User
from login.serializers import UserSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
 
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
                response["result"] = 1
                response["data"] = userProfileSerializer.data
                return Response(response, status=status.HTTP_201_CREATED)
        response["result"] = 0
        response["error"] = serializer.errors
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
