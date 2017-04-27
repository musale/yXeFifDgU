"""Loyalty URL Configuration."""
from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token as ShopkeeperLoginView

from .views import (AllCustomersForAShopkeeperListView, AllCustomersListView,
                    AllShopKeepersListView, ApiDocumentationView,
                    CustomerDetailView, CustomerForAShopkeeperDetailView,
                    ShopKeeperDetailView, ShopkeeperLogoutView,
                    SignUpCustomerApiView, SignUpShopkeeperApiView,
                    VerifyShopkeeperApiView)

urlpatterns = [
    url(r'^$',
        ApiDocumentationView.as_view(), name="apiv1_documentation"),
    url(r'^accounts/signup/shopkeepers/$',
        SignUpShopkeeperApiView.as_view(), name="accounts_signup_shopkeepers"),
    url(r'^accounts/signup/customers/$',
        SignUpCustomerApiView.as_view(), name="accounts_signup_customers"),
    url(r'^accounts/verify/shopkeepers/$',
        VerifyShopkeeperApiView.as_view(), name="accounts_verify_shopkeepers"),
    url(r'^accounts/login/$', ShopkeeperLoginView, name="accounts_login"),
    url(r'^accounts/logout/$',
        ShopkeeperLogoutView.as_view(), name="accounts_logout"),
    url(r'^customers/$',
        AllCustomersListView.as_view(), name="customers"),
    url(r'^customers/(?P<pk>[0-9]+)/$',
        CustomerDetailView.as_view(), name="customers_details"),
    url(r'^shopkeepers/$',
        AllShopKeepersListView.as_view(), name="shopkeepers"),
    url(r'^shopkeepers/(?P<pk>[0-9]+)/$',
        ShopKeeperDetailView.as_view(), name="shopkeepers_details"),
    url(r'^shopkeepers/(?P<pk>[0-9]+)/customers/$',
        AllCustomersForAShopkeeperListView.as_view(),
        name="shopkeepers_customers"),
    url(r'^shopkeepers/(?P<shopkeeper_pk>[0-9]+)/customers/(?P<pk>[0-9]+)/$',
        CustomerForAShopkeeperDetailView.as_view(),
        name="shopkeepers_customer_details"),
]
