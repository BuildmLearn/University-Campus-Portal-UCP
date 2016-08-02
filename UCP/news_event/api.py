"""
API file for news and event app

consists of the news list, detail and add api
events list, detail and add api
"""

from django.utils import timezone

from rest_framework import status, mixins
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets

from news_event.models import News, Event
from news_event.serializers import NewsSerializer, EventSerializer 


class NewsViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    

class EventViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    

