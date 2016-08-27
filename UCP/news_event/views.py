"""
Views file for News and Events App

contains views for the frontend pages of the News and Event App
"""

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from discussion.functions import get_all_tags
from news_event.models import News, Event
from news_event import functions
from UCP.functions import get_base_context
from UCP.settings import PAGE_SIZE


class NewsList(ListView):
    """
    Returns paginated list of all news articles
    If tag is send as a query, then the list is filtered by tag
    
    """
    model = News
    context_object_name = 'news_list'    
    paginate_by = PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        
        context['user'] = get_base_context(self.request)["user"]
        
        #add the list of page numbers to be displayed in the pagination at the bottom of the page
        news_list = self.get_queryset()
        count = len(news_list)
        page_count = count/PAGE_SIZE + 1
        context["pages"] = range(1, page_count+1)
        
        #if a tag is sent as a query, a link to subscribe to that tag is displayed at the top of the list
        #if the user already follows that tag, this link is not shown
        my_tags = [tag.name for tag in context['user'].followed_tags.all()]
        
        if 'tag' in self.request.GET and not self.request.GET["tag"] in my_tags:
            #tag added to the context to show follow link
            context['tag'] = self.request.GET["tag"]
            
        return context
        
    def get_queryset(self):
        """
        returns list of news article, filtered by tag or page number or both
        """
        if 'tag' in self.request.GET:
            news_list = News.objects.filter(tags__name = self.request.GET["tag"])
            count = len(news_list)
            page_count = count/PAGE_SIZE + 1
            if "page" in self.request.GET :
                page_no = int(self.request.GET["page"]) - 1
            else:
                page_no = 0
            offset = page_no * PAGE_SIZE
            news_list = news_list[offset:offset+PAGE_SIZE]
            ids = [news.pk for news in news_list]
            return News.objects.filter(pk__in=ids)
        else:
            return News.objects.all()


class NewsDetail(DetailView):
    """
    view for details page for a news article
    """
    model = News
    context_object_name = "news"
    
    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        return context
        

class EventList(ListView):
    """
    Returns paginated list of all events 
    If tag is send as a query, then the list is filtered by tag
    
    """
    model = Event
    context_object_name = 'events'    
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        news_list = self.get_queryset()
        count = len(news_list)
        page_count = count/PAGE_SIZE + 1
        context["pages"] = range(1, page_count+1)
        my_tags = [tag.name for tag in context['user'].followed_tags.all()]
        
        if 'tag' in self.request.GET and not self.request.GET["tag"] in my_tags:
            
            context['tag'] = self.request.GET["tag"]
            
        return context
        
    def get_queryset(self):
        if 'tag' in self.request.GET:
            events = Event.objects.approved().filter(tags__name = self.request.GET["tag"])
            count = len(events)
            page_count = count/PAGE_SIZE + 1
            if "page" in self.request.GET :
                page_no = int(self.request.GET["page"]) - 1
            else:
                page_no = 0
            offset = page_no * PAGE_SIZE
            events = events[offset:offset+PAGE_SIZE]
            ids = [event.pk for event in events]
            return Event.objects.approved().filter(pk__in=ids)
        else:
            return Event.objects.approved()


class EventDetail(DetailView):
    """
    returns detail page for an event
    """
    model = Event
    context_object_name = "event"
    
    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        return context
        
        
class EventCreate(View):
    """
    handles creation of an event
    """
    @method_decorator(login_required)
    def get(self, request):
        """
        returns the add event form
        """
        context = get_base_context(request)
        #tags used for the autocomplete feature of the tag input
        context["tags"] = get_all_tags()

        return render(request, 'news_event/add-event.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        """
        creates an event with the data send from the add event form
        """
        context = get_base_context(request)
        response = functions.add_event(request)
        
        if response["result"] == 1:
            return redirect('/events/')
        else:
            context["tags"] = get_all_tags()
            #if creation of event failed return to add event form with the errors
            return render(request, 'news_event/add-event.html', context)
        
        
class NewsCreate(View):
    """
    Handles creation of news
    accessible only to user with a moderator status
    """
    @method_decorator(login_required)
    def get(self, request):
        """
        returns add news form
        """
        context = get_base_context(request)
        #tags used for the autocomplete feature of the tag input
        context["tags"] = get_all_tags()

        return render(request, 'news_event/add-news.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        """
        creates a news article with data from the add news form
        """
        context = get_base_context(request)
        response = functions.add_news(request)
        
        if response["result"] == 1:
            return redirect('/news/')
        else:
            context["tags"] = get_all_tags()
            #if creation of event failed return to add event form with the errors
            return render(request, 'news_event/add-news.html', context)
    
        


        
    