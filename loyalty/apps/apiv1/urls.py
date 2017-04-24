"""Loyalty URL Configuration."""
from django.conf.urls import url

from .views import (SignUpCustomerApiView, SignUpShopkeeperApiView,
                    VerifyCustomerApiView)

urlpatterns = [
    url(r'^accounts/signup/shopkeepers/$',
        SignUpShopkeeperApiView.as_view(), name="accounts_signup_shopkeepers"),
    url(r'^accounts/signup/customers/$',
        SignUpCustomerApiView.as_view(), name="accounts_signup_customers"),
    url(r'^accounts/verify/shopkeepers/$',
        VerifyCustomerApiView.as_view(), name="accounts_verify_shopkeepers"),
]
