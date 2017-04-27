"""Loyalty URL Configuration."""
from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

from .views import (ApiDocumentationView, SignUpCustomerApiView,
                    SignUpShopkeeperApiView, VerifyShopkeeperApiView)

urlpatterns = [
    url(r'^$',
        ApiDocumentationView.as_view(), name="apiv1_documentation"),
    url(r'^accounts/signup/shopkeepers/$',
        SignUpShopkeeperApiView.as_view(), name="accounts_signup_shopkeepers"),
    url(r'^accounts/signup/customers/$',
        SignUpCustomerApiView.as_view(), name="accounts_signup_customers"),
    url(r'^accounts/verify/shopkeepers/$',
        VerifyShopkeeperApiView.as_view(), name="accounts_verify_shopkeepers"),
    url(r'^accounts/login/$', obtain_jwt_token, name="accounts_login"),
]
