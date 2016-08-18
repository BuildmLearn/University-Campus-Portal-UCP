"""
API file for discussion app

consists of the viewsets for the apis in the discussion app
"""

from django.utils import timezone

from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets

from discussion import functions
from discussion.models import DiscussionThread
from discussion.serializers import DiscussionThreadSerializer
from login.models import UserProfile


class DiscussionViewSet(viewsets.ViewSet):
    """
    Viewset for creating and retrieving discussion threads
    """
    
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
       
    @list_route(methods=['post'])
    def add(self, request):
        """
        Create a new discussion thread
        ---
        # YAML
        
        parameters:
            -   name: title
                description: Title for the thread
                required: true
                type: string
                paramType: form
            -   name: description
                description: description for the thread
                required: true
                type: string
                paramType: form
        """
        response = functions.add_discussion_thread(request)
    
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route()
    def get(self, request):
        """
        Get a list of all discussion threads
        ---
        # YAML
        
        parameters:
            -   name: page
                description: page no. of the results
                type: string
                paramType: query
        """
        
        response = functions.get_discussion_list(request)

        return Response(response, status=status.HTTP_200_OK)
        
    @list_route()
    def tags(self, request):
        """
        Get a list of all Tags matching the given query
        ---
        # YAML
        
        parameters:
            -   name: query
                type: string
                paramType: query
        """
        
        response = functions.get_tags(request.GET["query"])

        return Response(response, status=status.HTTP_200_OK)
    
    @detail_route(methods=['post'])
    def reply(self, request, pk):
        """
        Post a reply to a discussion thread
        ---
        # YAML
        
        parameters:
            -   name: text
                description: Title for the thread
                required: true
                type: string
                paramType: form
        """
        response = functions.add_reply(pk, request)
    
        return Response(response, status=status.HTTP_200_OK)
    
    @detail_route()
    def replies(self, request, pk):
        """
        Get all replies of a discussion thread
        ---
        # YAML
        
        parameters:
            -   name: page
                description: page no. of the results
                type: string
                paramType: query
        """
        response = functions.get_replies(pk, request)
    
        return Response(response, status=status.HTTP_200_OK)
    
    
    
    
    