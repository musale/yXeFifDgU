"""Loyalty URL Configuration."""
from django.conf.urls import url

from .views import SignUpApiView

urlpatterns = [
    url(r'^account/signup/$', SignUpApiView.as_view(), name="account_signup"),
]
