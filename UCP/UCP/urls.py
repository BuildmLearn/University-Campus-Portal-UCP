from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('restApi.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^user/', include('login.urls')),
]
