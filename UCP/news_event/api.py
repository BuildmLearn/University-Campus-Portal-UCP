"""
API file for news and event app

consists of the news list, detail and add api
events list, detail and add api
"""

from django.utils import timezone

from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets


class NewsViewSet(viewsets.ViewSet):
    pass
    

