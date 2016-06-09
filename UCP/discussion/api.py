"""
API file for login app

consists of the viewsets for the apis in the login app
"""

from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets

from discussion.models import DiscussionThread
from discussion.serializers import DiscussionThreadSerializer


class DiscussionViewSet(viewsets.ModelViewSet):
    """
    Viewset for creating and retrieving discussion threads
    """
    
    queryset = DiscussionThread.objects.all()
    serializer_class = DiscussionThreadSerializer
