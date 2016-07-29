from django.conf.urls import url
from news_event.views import NewsList, NewsDetail, EventList, EventDetail

urlpatterns = [
    url(r'^$', NewsList.as_view()),
    url(r'^(?P<pk>[0-9]+)$', NewsDetail.as_view(), name='news-detail'),
]