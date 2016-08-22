from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from result.serializers import ResultCreateSerializer, ResultSerializer
from UCP.constants import result
from UCP.settings import PAGE_SIZE
from result.models import Result

def get_top_results(tags):
    return Result.objects.filter(tags__in=tags)[:5]

def add_result(request):
    
    response = {}
    serializer = ResultCreateSerializer(data=request.POST)
        
    if serializer.is_valid():
        user_profile = UserProfile.objects.get(user = request.user)
        result_item = serializer.save(
            teacher = user_profile,
            result_file = request.FILES['result_file']
        )
        
        tags = request.POST["tag"].split(',')
        for tag_name in tags:
            if Tag.objects.filter(name = tag_name).exists():
                tag = Tag.objects.get(name = tag_name)
            else:
                tag = Tag(name=tag_name)
                tag.save()
            result_item.tags.add(tag)
        response["result"] = result.RESULT_SUCCESS
        response["error"] = []
    else:

        response["result"] = result.RESULT_FAILURE
        response["error"] = serializer.errors
    
    print response
    return response
    

def get_results(request):
    """
    Return a list of results filtered by page number and tag
    """
    response = {}
    
    threads = Result.objects.all()
    if "tag" in request.GET:
        #return a filtererd list
        threads = Result.objects.filter(tags__name = request.GET["tag"])
    
    #code for pagination
    count = len(threads)
    page_count = count/PAGE_SIZE + 1
    
    if("page" in request.GET):
        page_no = int(request.GET["page"]) - 1
    else:
        page_no = 0
    offset = page_no * PAGE_SIZE
    threads = threads[offset:offset+PAGE_SIZE]
    
    serializer = ResultSerializer(threads, many=True)

    response["page_count"] = page_count
    response["data"] = serializer.data
    
    return response
