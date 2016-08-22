from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from news_event.models import News, Event
from news_event.serializers import EventSerializer, NewsSerializer
from UCP.constants import result
from UCP.settings import PAGE_SIZE

def get_top_news(tags):
    return News.objects.filter(tags__in = tags)
    
def get_top_events(tags):
    return Event.objects.approved().filter(tags__in = tags)

def get_news(pk):
    """
    Return a news article with a given id pk
    """
    response = {}
    
    if not News.objects.filter(pk = pk):
        response["errors"] = ["news with given id doesnt exist"]
        response["result"] = result.RESULT_FAILURE
        return response
    
    news = News.objects.get(pk = pk)
    serializer = NewsSerializer(news)

    response["result"] = result.RESULT_SUCCESS
    response["data"] = serializer.data
    
    return response

def get_events(pk):
    """
    Return an event with a given id pk
    """
    response = {}
    
    if not Event.objects.filter(pk = pk):
        response["errors"] = ["event with given id doesnt exist"]
        response["result"] = result.RESULT_FAILURE
        return response
    
    event = Event.objects.get(pk = pk)
    serializer = EventSerializer(event)

    response["result"] = result.RESULT_SUCCESS
    response["data"] = serializer.data
    
    return response

def get_news_list(request):
    """
    Return a list of news filtered by page number and tag
    """
    response = {}
    
    threads = News.objects.all()
    if "tag" in request.GET:
        #return a filtererd list
        threads = News.objects.filter(tags__name = request.GET["tag"])
    
    #code for pagination
    count = len(threads)
    page_count = count/PAGE_SIZE + 1
    
    if("page" in request.GET):
        page_no = int(request.GET["page"]) - 1
    else:
        page_no = 0
    offset = page_no * PAGE_SIZE
    threads = threads[offset:offset+PAGE_SIZE]
    
    serializer = NewsSerializer(threads, many=True)

    response["page_count"] = page_count
    response["data"] = serializer.data
    
    return response
    
def get_events(request):
    """
    Return a list of events filtered by page number and tag
    """
    response = {}
    
    threads = Event.objects.all()
    if "tag" in request.GET:
        #return a filtererd list
        threads = Event.objects.filter(tags__name = request.GET["tag"])
    
    #code for pagination
    count = len(threads)
    page_count = count/PAGE_SIZE + 1
    
    if("page" in request.GET):
        page_no = int(request.GET["page"]) - 1
    else:
        page_no = 0
    offset = page_no * PAGE_SIZE
    threads = threads[offset:offset+PAGE_SIZE]
    
    serializer = EventSerializer(threads, many=True)

    response["page_count"] = page_count
    response["data"] = serializer.data
    
    return response

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

        tags = request.POST.get("tag","").split(',')
        for tag_name in tags:
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
            event.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["message"] = "event added successfully"
        response["errors"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["errors"] = serializer.errors
        
    return response
    
def add_news(request):
    
    response = {}
    serializer = NewsSerializer(data=request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        news = serializer.save(
            posted_by = user_profile
        )

        tags = request.POST.get("tag","").split(',')
        for tag_name in tags:
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
                
            news.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["message"] = "news added successfully"
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
        
    return response