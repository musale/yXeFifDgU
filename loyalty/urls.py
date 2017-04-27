"""Loyalty URL Configuration."""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('loyalty.apps.apiv1.urls', namespace="apiv1")),
]
