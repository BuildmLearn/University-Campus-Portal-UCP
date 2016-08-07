from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from schedule.serializers import ScheduleCreateSerializer
from UCP.constants import result

def add_schedule(request):
    
    response = {}
    serializer = ScheduleCreateSerializer(data=request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        item = serializer.save(
            teacher = user_profile,
            schedule_file = request.FILES['schedule_file']
        )
        
        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            tag = Tag(name=tag_name)
            tag.save()
            item.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
    
    return response
