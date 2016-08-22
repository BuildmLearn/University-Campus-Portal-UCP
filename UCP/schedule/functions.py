from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from schedule.serializers import ScheduleCreateSerializer, ScheduleSerializer
from schedule.models import Schedule
from UCP.constants import result
from UCP.settings import PAGE_SIZE


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

    

def get_schedules(request):
    """
    Return a list of schedules filtered by page number and tag
    """
    response = {}
    
    threads = Schedule.objects.all()
    if "tag" in request.GET:
        #return a filtererd list
        threads = Schedule.objects.filter(tags__name = request.GET["tag"])
    
    #code for pagination
    count = len(threads)
    page_count = count/PAGE_SIZE + 1
    
    if("page" in request.GET):
        page_no = int(request.GET["page"]) - 1
    else:
        page_no = 0
    offset = page_no * PAGE_SIZE
    threads = threads[offset:offset+PAGE_SIZE]
    
    serializer = ScheduleSerializer(threads, many=True)

    response["page_count"] = page_count
    response["data"] = serializer.data
    
    return response