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
    """
    returns a list of all availible tags
    """
    
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return serializer.data
    
def get_top_discussions(tags):
    """
    returns top 5 recent discussions from tags followed by the user
    """
    
    return DiscussionThread.objects.filter(tags__in = tags)[:5]

def add_discussion_thread(request):
    """
    """
    response = {}
    serializer = DiscussionThreadSerializer(data = request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        discussion = serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now()
        )

        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
                
            discussion.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
        response["message"] = "Discussion Thread added successfully"
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response
    
def get_discussion_list(request):
    """
    Return a list of discussion threads filtered by page number and tag
    """
    response = {}
    
    threads = DiscussionThread.objects.all()
    if "tag" in request.GET:
        #return a filtererd list
        threads = DiscussionThread.objects.filter(tags__name = request.GET["tag"])
    
    #code for pagination
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
    """
    subscribe request.user to a discussion thread with id pk
    """
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
    
def unsubscribe(request, pk):
    """
    unsubscribe request.user to a discussion thread with id pk
    """
    response = {}

    if DiscussionThread.objects.filter(id = pk).exists():
        discussion = DiscussionThread.objects.get(id = pk)
        
        user_profile = UserProfile.objects.get(user = request.user)
        discussion.subscribed.remove(user_profile)
        discussion.save()

        response["result"] = result.RESULT_SUCCESS
        return response
    else:
        response["result"] = result.RESULT_FAILURE
        response["error"] = "This discussion id does not exist"


def get_tags(query):
    """
    returns a list of tags whose name match the query
    """
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
    """
    returns all replies of a discussion pk based on the page number
    """
    response = {}
    
    if DiscussionThread.objects.filter(id = pk).exists():
        discussion = DiscussionThread.objects.get(id = pk)
        replies = Reply.objects.filter(thread = discussion)
        
        #pagination
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
    """
    Return the discussion with id pk
    """
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
        message += 'To view the discussions click here - '+discussion_url
        send_parallel_mail(discussion.title + " - new reply",message,[user.user.email])

def add_reply(pk, request):
    """
    add a reply to the discussion thread with id pk
    """
    response = {}
    
    discussion = DiscussionThread.objects.get(id = pk)
    discussion_serializer = DiscussionThreadSerializer(discussion)
    
    serializer = ReplySerializer(data=request.POST)
    
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        
        reply = serializer.save(
            posted_by = user_profile,
            posted_at = timezone.now(),
            thread = discussion
        )
        
        for _file in request.FILES.getlist('attachments'):
            print _file
            attachment = Attachment(
                reply = reply,
                uploaded_file = _file
            )
            attachment.save()
        
        
        discussion.no_of_replies += 1
        #automatically subscribe the person adding the reply to the discussion
        discussion.subscribed.add(user_profile)
        send_notification(discussion)
        discussion.save()
        
        response["result"] = result.RESULT_SUCCESS
        response["data"] = discussion_serializer.data
    else:
        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        response["data"] = discussion_serializer.data
        
    return response
    