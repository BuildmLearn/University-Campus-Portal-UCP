from django.conf.urls import url
from result.views import ResultList

urlpatterns = [
    url(r'^$', ResultList.as_view()),
]