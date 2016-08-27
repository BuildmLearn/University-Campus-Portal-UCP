from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from discussion.functions import get_all_tags

from schedule.models import Schedule
from schedule import functions
from UCP.functions import get_base_context
from UCP.settings import PAGE_SIZE

# Create your views here.


class ScheduleList(ListView):
    """
    Returns paginated list of schedules
    if tag is provided as a query, the list is filtered by that tag
    """
    model = Schedule
    context_object_name = 'schedules'    

    def get_context_data(self, **kwargs):
        context = super(ScheduleList, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        schedule_list = self.get_queryset()
        count = len(schedule_list)
        page_count = count/PAGE_SIZE + 1
        context["pages"] = range(1, page_count+1)
        my_tags = [tag.name for tag in context['user'].followed_tags.all()]
        
        if 'tag' in self.request.GET and not self.request.GET["tag"] in my_tags:
            
            context['tag'] = self.request.GET["tag"]
            
        return context
        
    def get_queryset(self):
        
        if 'tag' in self.request.GET:
            schedule_list = Schedule.objects.filter(tags__name = self.request.GET["tag"])
        else:
            schedule_list = Schedule.objects.all()
        
        count = len(schedule_list)
        page_count = count/PAGE_SIZE + 1
        if "page" in self.request.GET :
            page_no = int(self.request.GET["page"]) - 1
        else:
            page_no = 0
        offset = page_no * PAGE_SIZE
        schedule_list = schedule_list[offset:offset+PAGE_SIZE]
        ids = [schedule.pk for schedule in schedule_list]
        return Schedule.objects.filter(pk__in=ids)
        

class ScheduleCreate(View):
    """
    Handles creation of new schedules
    
    TO DO -
    restrict creation of schedules to users with a teacher status
    """
    @method_decorator(login_required)
    def get(self, request):
        context = get_base_context(request)
        context["tags"] = get_all_tags()

        return render(request, 'schedule/add_schedule.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        context = get_base_context(request)
        response = functions.add_schedule(request)
        
        if response["result"] == 1:
            return redirect('/schedule/')
        else:
            context["tags"] = get_all_tags()
            print response["error"]
            return render(request, 'schedule/add_schedule.html', context)    