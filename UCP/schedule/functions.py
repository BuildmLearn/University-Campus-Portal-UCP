from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from schedule.serializers import ScheduleCreateSerializer
from schedule.models import Schedule
from UCP.constants import result

def get_top_schedules(tags):
    return Schedule.objects.filter(tags__in = tags)[:5]

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
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
            item.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
    
    return response
