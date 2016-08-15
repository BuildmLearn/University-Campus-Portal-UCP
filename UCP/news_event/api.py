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

from UCP.constants import result

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
    
    queryset = Event.objects.approved()
    serializer_class = EventSerializer
    
    @detail_route(methods=['post'])
    def approve(self, request, pk):
        response = {}

        if Event.objects.pending().filter(id = pk).exists():
            event = Event.objects.get(id = pk)
            event.is_approved = True
            event.save()

            response["result"] = result.RESULT_SUCCESS
        else:
            response["result"] = result.RESULT_FAILURE
            response["error"] = "This Event id does not exist"
            
    
        return Response(response, status=status.HTTP_200_OK)
    
    
    def get_queryset(self):
        if self.action == "approve":
            return Event.objects.all()
        else:
            return Event.objects.approved()
            
    def get_serializer_class(self):
        if self.action == "approve":
            return None
        else:
            return EventSerializer
