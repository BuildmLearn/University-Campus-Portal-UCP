from django.conf.urls import include, patterns, url
from login import views

urlpatterns = [
    url(r'^register/', views.UserRegistration.as_view(), name='register'),
    url(r'^login/', views.UserLogin.as_view(), name='login'),
    url(r'^verify_email/', views.VerifyEmail.as_view(), name='verify_email'),
    url(r'^forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    url(r'^reset_password/', views.ResetPassword.as_view(), name='reset_password'),
]
