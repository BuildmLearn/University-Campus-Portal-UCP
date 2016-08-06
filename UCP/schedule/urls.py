from django.conf.urls import url
from schedule.views import ScheduleList

urlpatterns = [
    url(r'^$', ScheduleList.as_view()),
]