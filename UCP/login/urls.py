from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from login import frontend_views

urlpatterns = [
    url(r'^login/', frontend_views.Login.as_view(), name='login'),
    url(r'^register/', frontend_views.Register.as_view(), name='register'),
    url(r'^forgot_password/', frontend_views.ForgotPassword.as_view(), name='forgot_password'),
    url(r'^reset_password/', frontend_views.ResetPassword.as_view(), name='reset_password'),
]
