"""
functions.py file

contains functions common to all apps 
"""

from django.utils import timezone

def get_time_elapsed_string(date):
    """
    returns the time elapsed string based on the datetime object.
    ex:- 2 hours ago, 5 minutes ago
    """
    
    time_now = timezone.now()
    time_elapsed = time_now - date
    seconds_elapsed = time_elapsed.seconds
    
    if seconds_elapsed > 3600:
        hours_elapsed = seconds_elapsed/3600
        return str(hours_elapsed) + " hours ago"
    elif seconds_elapsed > 60:
        minutes_elapsed = seconds_elapsed/60
        return str(minutes_elapsed) + " minutes ago"
    else:
        return str(seconds_elapsed) + " seconds ago"
        