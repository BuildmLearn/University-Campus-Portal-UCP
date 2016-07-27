from django.shortcuts import render
from django.views.generic import ListView, DetailView

from news_event.models import News
# Create your views here.


class NewsList(ListView):
    model = News
    context_object_name = 'news_list'
    

class NewsDetail(DetailView):
    model = News
    context_object_name = "news"