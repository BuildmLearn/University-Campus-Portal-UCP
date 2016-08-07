from django.conf.urls import url
from result.views import ResultList, ResultCreate

urlpatterns = [
    url(r'^$', ResultList.as_view()),
    url(r'add/', ResultCreate.as_view()),
]