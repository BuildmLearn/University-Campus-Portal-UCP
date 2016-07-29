from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news_event.models import News
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
        return context
        
    