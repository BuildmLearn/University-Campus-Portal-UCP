"""
API file for result app

consists of the result list and add api
"""

from django.utils import timezone

from rest_framework import status, mixins
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets

from result.models import Result
from result.serializers import ResultSerializer, ResultCreateSerializer

class ResultViewSet(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    
    def create(self,request):
        """
        ---
        parameters:
            - name : result_file
              type : file
            - name : teacher
              type : int
            - name : tags
              description : tag ids seperated by commas
        """
        request.POST["tags"] = [1,2]
        return super(ResultViewSet, self).create(request)
    
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    
    def get_serializer_class(self):
        if self.action == "create":
            return ResultCreateSerializer
        else:
            return ResultSerializer