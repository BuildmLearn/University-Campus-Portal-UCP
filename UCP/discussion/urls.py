"""
Urls file for Discussion App

contains url patterns for the frontend pages of the discussion app
"""

from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from discussion import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)', views.DiscussionDetails.as_view(), name='discussion_detail'),
    url(r'^add_new_thread', views.AddDiscussion.as_view(), name='add-discussion'),
    url(r'^', views.DiscussionList.as_view(), name='discussion_list'),
]
