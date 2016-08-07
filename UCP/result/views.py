from django.shortcuts import render
from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from discussion.functions import get_all_tags

from result.models import Result
from result import functions

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
        

class ResultCreate(View):
    
    @method_decorator(login_required)
    def get(self, request):
        context = get_base_context(request)
        context["tags"] = get_all_tags()

        return render(request, 'result/add_result.html', context)
    
    @method_decorator(login_required)
    def post(self, request):
        context = get_base_context(request)
        response = functions.add_result(request)
        
        if response["result"] == 1:
            return redirect('/results/')
        else:
            context["tags"] = get_all_tags()
            print response["error"]
            return render(request, 'result/add_result.html', context)        
