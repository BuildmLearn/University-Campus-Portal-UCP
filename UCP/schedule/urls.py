from django.conf.urls import url
from schedule.views import ScheduleList, ScheduleCreate

urlpatterns = [
    url(r'^$', ScheduleList.as_view()),
    url(r'add/', ScheduleCreate.as_view()),
]