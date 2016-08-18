"""
Views file for Login App

contains views for the frontend pages of the Login App
"""

from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.views.generic import View


from discussion.functions import get_top_discussions
from discussion.models import Tag
from login.functions import login, register, forgot_password, reset_password, get_response_text, get_user_details, update_profile
from login.functions import get_user_profile, verify_email
from login.models import UserProfile
from news_event.functions import get_top_news, get_top_events
from result.functions import get_top_results
from schedule.functions import get_top_schedules
from news_event.models import Event
from UCP.constants import result
from UCP.functions import get_base_context


class Login(View):
    
    def get(self, request):
        context = {}
        context["is_login_page"] = True
        
        if request.user.is_authenticated() and UserProfile.objects.filter(user=request.user).exists():
            context = get_base_context(request)
            print context["user"].followed_tags.all()
            return render(request, 'home.html', context)
            
        return render(request, 'login-register.html', context)
        
        response = login(request)
        
        if response["result"] == result.RESULT_SUCCESS:
            context = get_base_context(request)
            return render(request, 'home.html', context)
        else:
            context["message"] = get_response_text(response)
        
            return render(request, 'login-register.html', context)
    
    def post(self, request):
        context = {}
        context["is_login_page"] = True
        
        if request.user.is_authenticated() and UserProfile.objects.filter(user=request.user).exists():
            context = get_base_context(request)
            return render(request, 'home.html', context)
        
        response = login(request)
        
        if response["result"] == result.RESULT_SUCCESS:
            context = get_base_context(request)
            return render(request, 'home.html', context)
        else:
            context["message"] = get_response_text(response)
        
            return render(request, 'login-register.html', context)


class Logout(View):
    
    def get(self, request):
        
        django_logout(request)
        return redirect('/user/login')


class Register(View):
    
    def get(self, request):
        return render(request, 'login-register.html')
        
    def post(self, request):

        context={}
        
        response = register(request)
        
        context["message"] = get_response_text(response)
        
        return render(request, 'login-register.html', context)


class ForgotPassword(View):
    
    def get(self, request):
        
        context={}
        response = forgot_password(request)
        context["message"] = get_response_text(response)
        
        if(response["result"] == 0):
            context["is_login_page"] = True
            print context
            return render(request, 'login-register.html', context)
        if(response["result"] == 1):
            return render(request, 'reset-password.html', context)


class ResetPassword(View):

   def post(self, request):

       context={}
       response = reset_password(request)
       context["message"] = get_response_text(response)

       if(response["result"] == 1):
           context["is_login_page"] = True
           return render(request, 'login-register.html', context)
       if(response["result"] == 0):
           return render(request, 'reset-password.html', context)


class PendingEvents(View):
    
    def get(self, request):
        
        context = {}
        user = get_user_details(request)
        context["user"] = user
        
        if not user["is_moderator"]:
            return redirect('/user/login/')
            
        context["pending_events"] = Event.objects.pending()
        return render(request, 'pending-events.html', context)


class ApproveEvent(View):
    
    def get(self, request, pk):
        user = get_user_details(request)
        context = {}
        
        context["user"] = user
        
        if not user["is_moderator"]:
            return redirect('/user/login/')
        
        
        Event.objects.filter(pk = pk).update(is_approved = True)
        context["pending_events"] = Event.objects.pending()
        
        return render(request, 'pending-events.html', context)


class RejectEvent(View):
    
    def get(self, request, pk):
        user = get_user_details(request)
        context = {}
        
        context["user"] = user
        
        if not user["is_moderator"]:
            return redirect('/user/login/')
        
        
        Event.objects.filter(pk = pk).update(is_approved = False)
        context["pending_events"] = Event.objects.pending()
        
        return render(request, 'pending-events.html', context)


class EditProfile(View):
    
    def get(self, request):
        
        context={}
        
        user = get_user_details(request)
        context["user"] = user
        if user["gender"] == "male":
            context["male"] = True
        else:
            context["male"] = False
        print user
        
        print context
        return render(request, 'edit-profile.html', context)
    
    def post(self, request):
        context={}
        
        response = update_profile(request)
        
        user = get_user_details(request)
        context["user"] = user
        if user["gender"] == "male":
            context["male"] = True
        else:
            context["male"] = False

       
        context["response"] = response
        
        return render(request, 'edit-profile.html', context)


class Profile(View):
    
    def get(self, request, pk):
        
        context=get_base_context(request)
        
        context['other_user'] = get_user_profile(pk)
        
        return render(request, 'profile.html', context)


class TagPage(View):
    
    def get(self, request):
        
        context=get_base_context(request)
        tag = Tag.objects.get(name = request.GET["tag"])
        context["tag"] = tag
        results = get_top_results([tag])
        schedules = get_top_schedules([tag])
        context["results"] = results
        context["schedules"] = schedules
        context["events"] = get_top_events([tag])
        
        context["news_list"] = get_top_news([tag])
        context["discussions"] = get_top_discussions([tag])
        
        return render(request, 'tag_page.html', context)


class VerificationPage(View):
    
    def get(self, request):
        
        context={}
        
        response = verify_email(request)
        
        context["response"] = response
        
        return render(request, 'email-verification.html', context)
        
        
        
        
