"""
Functions file for discussion app

consists of common functions used by both api.py and views.py file
"""
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

from login.models import UserProfile
import login.serializers as Serializers
from discussion.models import DiscussionThread, Reply
from discussion.serializers import DiscussionThreadSerializer, ReplySerializer
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL, PAGE_SIZE


def add_discussion_thread(request):
    
    response = {}
    serializer = DiscussionThreadSerializer(data=request.POST)

    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now()
        )
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response
    
def get_discussion_list(request):
    
    response = {}
    
    threads = DiscussionThread.objects.all()
    count = len(threads)
    if("page" in request.GET):
        page_no = int(request.GET["page"]) - 1
    else:
        page_no = 0
    offset = page_no * PAGE_SIZE
    threads = threads[offset:offset+PAGE_SIZE]
    
    serializer = DiscussionThreadSerializer(threads, many=True)

    response["count"] = count
    response["data"] = serializer.data
    
    return response
    
def get_replies(pk, request):
    
    response = {}
    
    if DiscussionThread.objects.filter(id = pk).exists():
        discussion = DiscussionThread.objects.get(id = pk)
        replies = Reply.objects.filter(thread = discussion)
        count = len(replies)
        if("page" in request.GET):
            page_no = int(request.GET["page"]) - 1
        else:
            page_no = 0
        offset = page_no * PAGE_SIZE
        replies = replies[offset:offset+PAGE_SIZE]
        
        reply_serializer = ReplySerializer(replies, many=True)
        discussion_serializer = DiscussionThreadSerializer(discussion)
        
        response["count"] = count
        response["data"] = {}
        response["data"]["discussion"] = discussion_serializer.data
        response["data"]["replies"] = reply_serializer.data
        
        return response
    else:
        response["error"] = "This discussion id does not exist"
        
def add_reply(pk, request):
    
    response = {}
    serializer = ReplySerializer(data=request.POST)

    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        discussion = DiscussionThread.objects.get(id = pk)
        
        serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now(),
            thread = discussion
        )
        response["error"] = []
    else:
        response["error"] = serializer.errors
        
    return response
    