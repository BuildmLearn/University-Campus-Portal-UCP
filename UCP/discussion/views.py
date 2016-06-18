"""
Views file for Discussions App

contains views for the frontend pages of the Discussions App
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator

from discussion import functions
from UCP.functions import get_time_elapsed_string

class DiscussionList(View):
    
    @method_decorator(login_required)
    def get(self, request):
        
        context={}
        response = functions.get_discussion_list(request)

        page_count = response["page_count"]
        
        context["pages"] = range(1, page_count+1)
        
        context["discussions"] = response["data"]
        
        return render(request, 'discussion-list.html', context)
        
        
class DiscussionDetails(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        
        context={}
        
        response = functions.get_replies(pk, request)
        page_count = response["page_count"]
        context["pages"] = range(1, page_count+1)
        context["replies"] = response["data"]["replies"]
        context["discussion"] = response["data"]["discussion"]
        print context
        return render(request, 'discussion-detail.html', context)
        
        
class AddDiscussion(View):
    
    @method_decorator(login_required)
    def get(self, request):
        
        return render(request, 'add-discussion.html')
    
    @method_decorator(login_required)
    def post(self, request):
        
        response = functions.add_discussion_thread(request)
        
        if response["result"] == 1:
            return redirect('/discussions/')
        else:
            print response
            return render(request, 'add-discussion.html')        
        
        
class Reply(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        context = {}
        
        response = functions.get_discussion(pk)
        context["discussion"] = response["data"]
        
        return render(request, 'reply.html', context)
    
    @method_decorator(login_required)
    def post(self, request, pk):
        context = {}
        
        response = functions.add_reply(pk, request)
        context["discussion"] = response["data"]
        
        if response["result"] == 1:
            return redirect('/discussions/'+str(pk))
        else:
            print response
            return render(request, 'reply.html', context)