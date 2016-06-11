"""
Views file for Discussions App

contains views for the frontend pages of the Discussions App
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator

from discussion import functions


class DiscussionList(View):
    
    @method_decorator(login_required)
    def get(self, request):
        
        context={}
        print request.user
        response = functions.get_discussion_list(request)
        
        context["discussions"] = response["data"]
        
        return render(request, 'discussion-list.html', context)
        
        
class DiscussionDetails(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        
        context={}
        
        response = functions.get_replies(pk, request)
        
        context["replies"] = response["data"]
        
        return render(request, 'discussion-detail.html', context)
        
        
class AddDiscussion(View):
    
    @method_decorator(login_required)
    def get(self, request):
        
        return render(request, 'add-discussion.html')
    
    @method_decorator(login_required)
    def post(self, request):
        print(request.POST)
        return render(request, 'add-discussion.html')