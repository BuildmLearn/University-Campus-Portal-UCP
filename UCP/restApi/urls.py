from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

urlpatterns = [
    url(r'^user/', include('login.user_urls')),
    url(r'^password/', include('login.password_urls')),
]
