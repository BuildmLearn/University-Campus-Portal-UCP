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

from discussion.models import Tag
from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer, ScheduleCreateSerializer

from UCP.constants import result

class ScheduleViewSet(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    
    def create(self,request):
        """
        ---
        parameters:
            - name : schedule_file
              type : file
            - name : teacher
              type : int
            - name : tags
              type : string
              description : tag ids seperated by commas
        """
        response = {}
        serializer = ScheduleCreateSerializer(data = request.POST)
        if serializer.is_valid():
            schedule = serializer.save()
            tag_ids = [ int(t) for t in request.POST["tags"].split(",") ]
            tags = Tag.objects.filter(pk__in = tag_ids)
            schedule.tags = tags
            schedule.save()
            serializer = ScheduleSerializer(schedule)
            response["result"] = result.RESULT_SUCCESS
            response["data"] = serializer.data
        else:
            response["result"] = result.RESULT_FAILURE
            response["errors"] = serializer.errors
        return Response(response, status=status.HTTP_200_OK)
    
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    def get_serializer_class(self):
        if self.action == "create":
            return ScheduleCreateSerializer
        else:
            return ScheduleSerializer