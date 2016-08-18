from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from login.api import UserViewSet, UserPasswordViewSet
from login.views import Login, ApproveEvent
from discussion.api import DiscussionViewSet
from result.api import ResultViewSet
from schedule.api import ScheduleViewSet

from news_event.api import NewsViewSet, EventViewSet
from news_event.views import NewsList, NewsDetail, EventList, EventDetail, EventCreate, NewsCreate
from discussion.views import FollowTag

router = DefaultRouter()
router.register(r'user', UserViewSet, base_name="Authentication")
router.register(r'password', UserPasswordViewSet, base_name="Passwords")
router.register(r'discussions', DiscussionViewSet, base_name="Discussions")
router.register(r'news', NewsViewSet, base_name="News")
router.register(r'events', EventViewSet, base_name="Events")
router.register(r'results', ResultViewSet, base_name="Results")
router.register(r'schedule', ScheduleViewSet, base_name="Schedule")

urlpatterns = []

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^user/', include('login.urls')),
    url(r'^tag/follow/', FollowTag.as_view()),
    url(r'^discussions/', include('discussion.urls')),
    url(r'^results/', include('result.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^news/add/', NewsCreate.as_view()),
    url(r'^news/(?P<pk>[0-9]+)$', NewsDetail.as_view(), name='news-detail'),
    url(r'^news/', NewsList.as_view()),
    url(r'^news/(?P<pk>[0-9]+)$', NewsDetail.as_view(), name='news-detail'),
    url(r'^events/add/', EventCreate.as_view()),
    url(r'^events/approve/(?P<pk>[0-9]+)$', ApproveEvent.as_view(), name='approve-event'),
    url(r'^events/(?P<pk>[0-9]+)$', EventDetail.as_view(), name='news-detail'),
    url(r'^events/', EventList.as_view()),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^', Login.as_view()),
    url(r'^tinymce/',include('tinymce.urls')),
]
