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
from discussion.models import DiscussionThread, Reply, Attachment
from discussion.serializers import DiscussionThreadSerializer,DiscussionThreadFullSerializer, ReplySerializer, ReplyFullSerializer
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
    page_count = count/PAGE_SIZE + 1
    
    if("page" in request.GET):
        page_no = int(request.GET["page"]) - 1
    else:
        page_no = 0
    offset = page_no * PAGE_SIZE
    threads = threads[offset:offset+PAGE_SIZE]
    
    serializer = DiscussionThreadFullSerializer(threads, many=True)

    response["page_count"] = page_count
    response["data"] = serializer.data
    
    return response
    
def get_replies(pk, request):
    
    response = {}
    
    if DiscussionThread.objects.filter(id = pk).exists():
        discussion = DiscussionThread.objects.get(id = pk)
        replies = Reply.objects.filter(thread = discussion)
        page_count = len(replies)/PAGE_SIZE + 1
        if("page" in request.GET):
            page_no = int(request.GET["page"]) - 1
        else:
            page_no = 0
        offset = page_no * PAGE_SIZE
        replies = replies[offset:offset+PAGE_SIZE]
        
        reply_serializer = ReplyFullSerializer(replies, many=True)
        discussion_serializer = DiscussionThreadFullSerializer(discussion)
        
        response["page_count"] = page_count
        response["data"] = {}
        response["data"]["discussion"] = discussion_serializer.data
        response["data"]["replies"] = reply_serializer.data
        
        return response
    else:
        response["error"] = "This discussion id does not exist"
        
def get_discussion(pk):
    
    response = {}
    discussion = DiscussionThread.objects.get(id = pk)
    serializer = DiscussionThreadSerializer(discussion)
    
    response["data"] = serializer.data
    
    return response

def add_reply(pk, request):
    
    response = {}
    serializer = ReplySerializer(data=request.POST)
    
    discussion = DiscussionThread.objects.get(id = pk)
        
    discussion_serializer = DiscussionThreadSerializer(discussion)
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        
        reply = serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now(),
            thread = discussion
        )
        print "--"*40
        print request.FILES.getlist('attachments') 
        
        for _file in request.FILES.getlist('attachments'):
            print _file
            attachment = Attachment(
                reply = reply,
                uploaded_file = _file
            )
            attachment.save()
        
        
        discussion.no_of_replies += 1
        discussion.save()
        
        response["result"] = 1
        response["data"] = discussion_serializer.data
    else:
        response["result"] = 0
        response["error"] = serializer.errors
        response["data"] = discussion_serializer.data
        
    return response
    