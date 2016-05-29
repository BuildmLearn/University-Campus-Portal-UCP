from django.conf.urls import include, patterns, url
from login import views

urlpatterns = [
    url(r'^forgot/', views.ForgotPassword.as_view(), name='forgot_password'),
    url(r'^reset/', views.ResetPassword.as_view(), name='reset_password'),
]
