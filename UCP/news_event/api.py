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

from news_event import functions
from news_event.models import News, Event
from news_event.serializers import NewsSerializer, EventSerializer 

from UCP.constants import result


class NewsViewSet(viewsets.ViewSet):
    """
    Viewset for creating and listing results
    """
    
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    
    @list_route(methods=['POST'])
    def add(self,request):
        """
        Add a new News article
        ---
        parameters:
            - name : tags
              type : string
              description : tag ids seperated by commas
        """
        response = functions.add_news(request)
        
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route()
    def get(self, request):
        """
        Get a list of all Schedules
        ---
        # YAML
        
        parameters:
            -   name: page
                description: page no. of the news list
                type: string
                paramType: query
        """
        
        response = functions.get_news_list(request)

        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        """
        Get full details of a news article with id pk
        """
        
        response = functions.get_news(pk)
        return Response(response, status=status.HTTP_200_OK)
    
    def get_serializer_class(self):
        if self.action == "add":
            return NewsSerializer
        else:
            return NewsSerializer


class EventViewSet(viewsets.ViewSet):
    
    serializer_class = EventSerializer
    
    @list_route(methods=['POST'])
    def add(self,request):
        """
        Add a new event article
        ---
        parameters:
            - name : tags
              type : string
              description : tag ids seperated by commas
        """
        response = functions.add_event(request)
        
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route()
    def get(self, request):
        """
        Get a list of all events
        ---
        # YAML
        
        parameters:
            -   name: page
                description: page no. of the events
                type: string
                paramType: query
        """
        
        response = functions.get_events(request)

        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        """
        Get full details of a news article with id pk
        """
        
        response = functions.get_events(pk)
        return Response(response, status=status.HTTP_200_OK)
        
    @detail_route(methods=['post'])
    def approve(self, request, pk):
        """
        approve a event
        """
        response = {}

        if Event.objects.pending().filter(id = pk).exists():
            event = Event.objects.get(id = pk)
            event.is_approved = True
            event.save()

            response["result"] = result.RESULT_SUCCESS
        else:
            response["result"] = result.RESULT_FAILURE
            response["errors"] = ["This Event id does not exist"]
            
    
        return Response(response, status=status.HTTP_200_OK)
    
    @detail_route(methods=['post'])
    def reject(self, request, pk):
        """
        reject a event
        """
        response = {}

        if Event.objects.pending().filter(id = pk).exists():
            event = Event.objects.get(id = pk)
            event.is_approved = True
            event.save()

            response["result"] = result.RESULT_SUCCESS
        else:
            response["result"] = result.RESULT_FAILURE
            response["errors"] = ["This Event id does not exist"]
            
    
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route()
    def pending(self, request):
        """
        Get list of pending events
        """
        response = {}
        events = Event.objects.pending()
        response["result"] = result.RESULT_SUCCESS
        response["data"] = EventSerializer(events, many=True).data
        
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
