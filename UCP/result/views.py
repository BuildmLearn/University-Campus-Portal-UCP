from django.shortcuts import render
from django.views.generic import ListView

from result.models import Result

from UCP.functions import get_base_context
from UCP.settings import PAGE_SIZE

# Create your views here.


class ResultList(ListView):
    
    model = Result
    context_object_name = 'results'    

    def get_context_data(self, **kwargs):
        context = super(ResultList, self).get_context_data(**kwargs)
        context['user'] = get_base_context(self.request)["user"]
        result_list = self.get_queryset()
        count = len(result_list)
        page_count = count/PAGE_SIZE + 1
        context["pages"] = range(1, page_count+1)
        return context
        
    def get_queryset(self):
        
        if 'tag' in self.request.GET:
            result_list = Result.objects.filter(tags__name = self.request.GET["tag"])
        else:
            result_list = Result.objects.all()
        
        count = len(result_list)
        page_count = count/PAGE_SIZE + 1
        if "page" in self.request.GET :
            page_no = int(self.request.GET["page"]) - 1
        else:
            page_no = 0
        offset = page_no * PAGE_SIZE
        result_list = result_list[offset:offset+PAGE_SIZE]
        ids = [result.pk for result in result_list]
        return Result.objects.filter(pk__in=ids)
        
