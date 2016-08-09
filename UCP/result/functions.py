from django.utils import timezone

from discussion.models import Tag
from login.models import UserProfile
from result.serializers import ResultCreateSerializer
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
