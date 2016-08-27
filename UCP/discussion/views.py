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
    """
    This view class handles displaying a paginated list of all discussion threads
    """
    @method_decorator(my_login_required)
    def get(self, request):
        """
        returns discussion list, if a tag is sent as a query, the list of discussions is filtered by that tag
        
        """
        context = get_base_context(request)

        response = functions.get_discussion_list(request)

        page_count = response["page_count"]
        #page numers to be displayed in the pagination at the bottom of the page
        context["pages"] = range(1, page_count+1)

        #if a tag is sent as a query, a link to subscribe to that tag is displayed at the top of the list
        #if the user already follows that tag, this link is not shown
        my_tags = [tag.name for tag in context['user'].followed_tags.all()]
        
        if 'tag' in self.request.GET and not self.request.GET["tag"] in my_tags:
            #tag added to the context to show follow link
            context['tag'] = self.request.GET["tag"]
            
            
        context["discussions"] = response["data"]

        return render(request, 'discussion-list.html', context)
        
        
class DiscussionDetails(View):
    """
    handles displaying full disscussion thread details along with a paginated list of all replies
    """
    @method_decorator(login_required)
    def get(self, request, pk):
        
        context = get_base_context(request)
        
        discussion = DiscussionThread.objects.get(id=pk)
        userProfile = UserProfile.objects.get(user = request.user)
        response = functions.get_replies(pk, request)
        page_count = response["page_count"]
        #if user is already subscribed to the discussion, unsubscribe button is displayed
        context["subscribed"] = (userProfile in discussion.subscribed.all())
        
        #list of page numbers to be displayed at the pagination in the bottom of the page
        context["pages"] = range(1, page_count+1)
        
        context["replies"] = response["data"]["replies"]
        
        context["discussion"] = response["data"]["discussion"]
        
        return render(request, 'discussion-detail.html', context)
        
        
class AddDiscussion(View):
    """
    handles addition of a discussion thread
    """
    @method_decorator(login_required)
    def get(self, request):
        """
        returns discussion add form
        """
        context = get_base_context(request)
        # list of all tags added to the portal, used by the tagit field for autocomplete suggestions
        context["tags"] = functions.get_all_tags()
        print context
        return render(request, 'add-discussion.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        """
        adds a discussion thread with data send from the add discussion form
        If unable to create the thread, it returns the discussion form with a list of errors
        """
        context = get_base_context(request)
        
        response = functions.add_discussion_thread(request)
        
        if response["result"] == 1:
            return redirect('/discussions/')
        else:
            
            return render(request, 'add-discussion.html', context)        
        
        
class Reply(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        """
        returns add reply form for discussion with id pk
        Note - this function is no longer used as the add discussion form is moved to the discussion details page
        """
        context = get_base_context(request)
        
        response = functions.get_discussion(pk)
        context["discussion"] = response["data"]
        
        return render(request, 'reply.html', context)
    
    @method_decorator(login_required)
    def post(self, request, pk):
        """
        Adds a reply to discussion thread with id pk
        """
        context = get_base_context(request)
        
        response = functions.add_reply(pk, request)
        context["discussion"] = response["data"]
        
        if response["result"] == 1:
            return redirect('/discussions/'+str(pk))
        else:
            print response
            return render(request, 'reply.html', context)        
        

class FollowTag(View):
    
    @method_decorator(login_required)
    def get(self, request):
        """
        Adds a tag to the followed tags of the logged in user
        redirects to the home page which displays the list of the users followed tags
        """
        tag = Tag.objects.get(name = request.GET['tag'])
        userProfile = UserProfile.objects.get(user = request.user)
        userProfile.followed_tags.add(tag)
        userProfile.save()
        return redirect('/')

class Subscribe(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        """
        Subscribe the user to email notifications about a discussion
        """
        response = functions.subscribe(request, pk)
        
        return redirect('/discussions/'+str(pk))        
        

class UnSubscribe(View):
    
    @method_decorator(login_required)
    def get(self, request, pk):
        """
        Unsubscribe the user to email notifications about a discussion
        """
        response = functions.unsubscribe(request, pk)
        
        return redirect('/discussions/'+str(pk))
    