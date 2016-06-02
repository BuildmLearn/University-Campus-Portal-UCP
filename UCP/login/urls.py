from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from login import frontend_views

urlpatterns = [
    url(r'^login/', frontend_views.Login.as_view(), name='login')
]
