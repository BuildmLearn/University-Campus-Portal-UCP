from django.conf.urls import include, patterns, url
from login import views

urlpatterns = [
    url(r'^register/', views.UserRegistration.as_view(), name='register'),
    url(r'^login/', views.UserLogin.as_view(), name='login'),
    url(r'^verify_email/', views.VerifyEmail.as_view(), name='verify_email'),
]
