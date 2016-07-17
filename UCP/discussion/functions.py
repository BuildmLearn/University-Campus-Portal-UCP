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
from discussion.models import DiscussionThread, Reply, Attachment, Tag
from discussion.serializers import DiscussionThreadSerializer,DiscussionThreadFullSerializer, ReplySerializer, ReplyFullSerializer, TagSerializer
from UCP.constants import result, message
from UCP.settings import EMAIL_HOST_USER, BASE_URL, PAGE_SIZE
from UCP.functions import send_parallel_mail


def get_all_tags():
    "returns a list of all availible tags"
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return serializer.data
    
def add_discussion_thread(request):
    
    response = {}
    serializer = DiscussionThreadSerializer(data=request.POST)
    
    print request.POST
    
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        discussion = serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now()
        )

        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            tag = Tag(name=tag_name)
            tag.save()
            discussion.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response
    
def get_discussion_list(request):
    
    response = {}
    
    threads = DiscussionThread.objects.all()
    if "tag" in request.GET:
        threads = DiscussionThread.objects.filter(tags__name = request.GET["tag"])
        
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
    
def subscribe(request, pk):
    response = {}

    if DiscussionThread.objects.filter(id = pk).exists():
        discussion = DiscussionThread.objects.get(id = pk)
        
        user_profile = UserProfile.objects.get(user = request.user)
        discussion.subscribed.add(user_profile)
        discussion.save()

        response["result"] = result.RESULT_SUCCESS
        return response
    else:
        response["result"] = result.RESULT_FAILURE
        response["error"] = "This discussion id does not exist"


def get_tags(query):
    """returns a list of tags whose name match the query"""
    tags = Tag.objects.filter(name__icontains=query)
    data = []
    for tag in tags:
        item = {}
        item["id"] = tag.id
        item["value"] = tag.name
        item["label"] = tag.name
        data.append(item)
    return data
    
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

def send_notification(discussion):
    """
    send an email notification to people subscribed to a thread
    """
    for user in discussion.subscribed.all():
        discussion_url = "http://" + BASE_URL + "/discussions/" + str(discussion.id)
        message  = "Hey "+user.user.first_name + "!\n"
        message += "A new reply was added to this discussion\n"
        message += 'To view the discussions click <a href="'+discussion_url+'">here</a>'
        print message
        send_parallel_mail(discussion.title + " - new reply",message,[user.user.email])

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
        
        for _file in request.FILES.getlist('attachments'):
            print _file
            attachment = Attachment(
                reply = reply,
                uploaded_file = _file
            )
            attachment.save()
        
        
        discussion.no_of_replies += 1
        discussion.subscribed.add(user_profile)
        send_notification(discussion)
        discussion.save()
        
        
        response["result"] = 1
        response["data"] = discussion_serializer.data
    else:
        response["result"] = 0
        response["error"] = serializer.errors
        response["data"] = discussion_serializer.data
        
    return response
    