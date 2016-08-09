"""
Urls file for Login App

contains url patterns for the frontend pages of the login app
"""

from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView

from login import views

urlpatterns = [
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout', views.Logout.as_view(), name='logout'),
    url(r'^register/', views.Register.as_view(), name='register'),
    url(r'^forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    url(r'^reset_password/', views.ResetPassword.as_view(), name='reset_password'),
    url(r'^edit_profile', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^verify_email', views.VerificationPage.as_view(), name='verify_email'),
    url(r'^(?P<pk>[0-9]+)', views.Profile.as_view(), name='profile'),
    url(r'^tag_page/', views.TagPage.as_view(), name='tag_page'),
]
