from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from news_event.models import News, Event
from news_event.serializers import EventSerializer, NewsSerializer
from UCP.constants import result

def get_top_news(tags):
    return News.objects.filter(tags__in = tags)
    
def get_top_events(tags):
    return Event.objects.filter(tags__in = tags)

def add_event(request):
    
    response = {}
    serializer = EventSerializer(data=request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        if 'image' in request.FILES:
            event = serializer.save(
                posted_by = user_profile,
                image = request.FILES['image']
            )
        else:
            event = serializer.save(
                posted_by = user_profile
            )

        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
            event.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response
    
def add_news(request):
    
    response = {}
    serializer = NewsSerializer(data=request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        news = serializer.save(
            posted_by = user_profile
        )

        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
                
            news.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response