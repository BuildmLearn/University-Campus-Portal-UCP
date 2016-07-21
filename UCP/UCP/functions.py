"""
functions.py file

contains functions common to all apps 
"""
import thread

from django.core.mail import send_mail
from django.utils import timezone
from login.models import UserProfile
from login.serializers import UserProfileFullSerializer
from UCP.settings import EMAIL_HOST_USER


def get_time_elapsed_string(date):
    """
    returns the time elapsed string based on the datetime object.
    ex:- 2 hours ago, 5 minutes ago
    """
    
    time_now = timezone.now()
    time_elapsed = time_now - date
    seconds_elapsed = time_elapsed.seconds
    
    if time_elapsed.days > 0:
        days_elapsed = time_elapsed.days
        return str(days_elapsed) + " days ago"
    elif seconds_elapsed > 3600:
        hours_elapsed = seconds_elapsed/3600
        return str(hours_elapsed) + " hours ago"
    elif seconds_elapsed > 60:
        minutes_elapsed = seconds_elapsed/60
        return str(minutes_elapsed) + " minutes ago"
    else:
        return str(seconds_elapsed) + " seconds ago"
        

def get_file_size_string(size):
    """
    returns the size in kbs 
    """
    
    size_in_kb = "{0:.3f}".format(size/1000.0)
    return str(size_in_kb) + " kb"
    

def get_base_context(request):
    """
    returns a base context with user details to be sent to a template
    """
    user = UserProfile.objects.get(user=request.user)
    serializer = UserProfileFullSerializer(user)
    
    context = {}
    context["user"] = serializer.data
    
    return context
    

def send_parallel_mail(sub,msg,to):
    thread.start_new_thread( send_mail, (sub, msg, EMAIL_HOST_USER, to) )
    
    