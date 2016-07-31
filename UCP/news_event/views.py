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
# Create your views here.


class NewsList(ListView):
    
    model = News
    context_object_name = 'news_list'    
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        news_list = self.get_queryset()
        count = len(news_list)
        page_count = count/PAGE_SIZE + 1
        context["pages"] = range(1, page_count+1)
        return context
        
    def get_queryset(self):
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
    
    model = News
    context_object_name = "news"
    
    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        print context
        return context
        

class EventList(ListView):
    
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
        return context
        
    def get_queryset(self):
        if 'tag' in self.request.GET:
            events = Event.objects.filter(tags__name = self.request.GET["tag"])
            count = len(events)
            page_count = count/PAGE_SIZE + 1
            if "page" in self.request.GET :
                page_no = int(self.request.GET["page"]) - 1
            else:
                page_no = 0
            offset = page_no * PAGE_SIZE
            events = events[offset:offset+PAGE_SIZE]
            ids = [event.pk for event in events]
            return Event.objects.filter(pk__in=ids)
        else:
            return Event.objects.all()


class EventDetail(DetailView):
    
    model = Event
    context_object_name = "event"
    
    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        return context
        
        
class EventCreate(View):
    
    @method_decorator(login_required)
    def get(self, request):
        context = get_base_context(request)
        context["tags"] = get_all_tags()

        return render(request, 'news_event/add-event.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        context = get_base_context(request)
        response = functions.add_event(request)
        
        if response["result"] == 1:
            return redirect('/events/')
        else:
            context["tags"] = get_all_tags()
            print response["error"]
            return render(request, 'news_event/add-event.html', context)
        
        
class NewsCreate(View):
    
    @method_decorator(login_required)
    def get(self, request):
        context = get_base_context(request)
        context["tags"] = get_all_tags()

        return render(request, 'news_event/add-news.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        context = get_base_context(request)
        response = functions.add_news(request)
        
        if response["result"] == 1:
            return redirect('/news/')
        else:
            context["tags"] = get_all_tags()
            print response["error"]
            return render(request, 'news_event/add-news.html', context)
    
        


        
    