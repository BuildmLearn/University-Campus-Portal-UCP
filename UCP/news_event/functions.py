from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from news_event.serializers import EventSerializer
from UCP.constants import result

def add_event(request):
    
    response = {}
    serializer = EventSerializer(data=request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        event = serializer.save(
            posted_by = user_profile,
        )

        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            tag = Tag(name=tag_name)
            tag.save()
            event.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response