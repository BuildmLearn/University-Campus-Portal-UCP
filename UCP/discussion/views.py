"""
Views file for Discussions App

contains views for the frontend pages of the Discussions App
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator

from discussion import functions
from discussion.models import DiscussionThread, Tag
from login.models import UserProfile
from UCP.functions import get_time_elapsed_string, get_base_context, my_login_required


class DiscussionList(View):
    
    @method_decorator(my_login_required)
    def get(self, request):
        
        context = get_base_context(request)

        response = functions.get_discussion_list(request)

        page_count = response["page_count"]
        
        context["pages"] = range(1, page_count+1)

        if 'tag' in self.request.GET:
            context["tag"] = self.request.GET["tag"]
            
        context["discussions"] = response["data"]

        return render(request, 'discussion-list.html', context)
        
        
class DiscussionDetails(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        
        context = get_base_context(request)
        discussion = DiscussionThread.objects.get(id=pk)
        userProfile = UserProfile.objects.get(user = request.user)
        response = functions.get_replies(pk, request)
        page_count = response["page_count"]
        context["subscribed"] = (userProfile in discussion.subscribed.all())
        context["pages"] = range(1, page_count+1)
        context["replies"] = response["data"]["replies"]
        context["discussion"] = response["data"]["discussion"]
        
        return render(request, 'discussion-detail.html', context)
        
        
class AddDiscussion(View):
    
    @method_decorator(login_required)
    def get(self, request):
        
        context = get_base_context(request)
        context["tags"] = functions.get_all_tags()
        print context
        return render(request, 'add-discussion.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        
        context = get_base_context(request)
        
        response = functions.add_discussion_thread(request)
        
        if response["result"] == 1:
            return redirect('/discussions/')
        else:
            print response
            return render(request, 'add-discussion.html', context)        
        
        
class Reply(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        context = get_base_context(request)
        
        response = functions.get_discussion(pk)
        context["discussion"] = response["data"]
        
        return render(request, 'reply.html', context)
    
    @method_decorator(login_required)
    def post(self, request, pk):
        context = get_base_context(request)
        
        response = functions.add_reply(pk, request)
        context["discussion"] = response["data"]
        
        print request.FILES
        if response["result"] == 1:
            return redirect('/discussions/'+str(pk))
        else:
            print response
            return render(request, 'reply.html', context)        
        

class FollowTag(View):
    
    @method_decorator(login_required)
    def get(self, request):
        tag = Tag.objects.get(name = request.GET['tag'])
        userProfile = UserProfile.objects.get(user = request.user)
        userProfile.followed_tags.add(tag)
        userProfile.save()
        return redirect('/')

class Subscribe(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        response = functions.subscribe(request, pk)
        
        return redirect('/discussions/'+str(pk))        
        

class UnSubscribe(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        response = functions.unsubscribe(request, pk)
        
        return redirect('/discussions/'+str(pk))
    