"""
Views file for Discussions App

contains views for the frontend pages of the Discussions App
"""

from django.shortcuts import render
from django.views.generic import View

from discussion import functions


class DiscussionList(View):
    
    def get(self, request):
        
        context={}
        
        response = functions.get_discussion_list(request)
        
        context["discussions"] = response["data"]
        
        return render(request, 'discussion-list.html', context)
        
        
class DiscussionDetails(View):
    
    def get(self, request, pk):
        
        context={}
        
        response = functions.get_replies(pk, request)
        
        context["replies"] = response["data"]
        
        return render(request, 'discussion-detail.html', context)
        
        
class AddDiscussion(View):
    
    def get(self, request):
        
        return render(request, 'add-discussion.html')
        
    def post(self, request):
        print(request.POST)
        return render(request, 'add-discussion.html')