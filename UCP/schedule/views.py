from django.shortcuts import render
from django.views.generic import ListView

from schedule.models import Schedule

from UCP.functions import get_base_context
from UCP.settings import PAGE_SIZE

# Create your views here.


class ScheduleList(ListView):
    
    model = Schedule
    context_object_name = 'schedules'    

    def get_context_data(self, **kwargs):
        context = super(ScheduleList, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        schedule_list = self.get_queryset()
        count = len(schedule_list)
        page_count = count/PAGE_SIZE + 1
        context["pages"] = range(1, page_count+1)
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
        
# Create your views here.
