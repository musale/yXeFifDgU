"""API version 1 for dukaconnect loyalty."""
from __future__ import unicode_literals

import datetime
# from django.http import Http404
from logging import getLogger

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from loyalty.apps.account.models import Customer
from utils.utilities import generate_code

logger = getLogger(__name__)


@permission_classes((AllowAny, ))
class SignUpApiView(APIView):
    """Sign up a shopkeeper or a customer."""

    http_method_names = ['post']

    def post(self, request, format=None):
        """Handle POST account/signup/ ."""
        data = request.data
        user_type = data.get("user_type" or None)
        # generate new code and expiry date for the shopkeeper
        code, day = generate_code()
        if user_type == "SHOPKEEPER":
            user = save_new_shopkeeper(data)
            # save shopkeeper
            user.userprofile.user_type = user_type
            # save the code and expiry date
            user.userprofile.activation_key = code
            user.userprofile.key_expiry_date = day
            user.save()
        elif user_type == "CUSTOMER":
            # save a customer
            customer = save_new_customer(data)
            if customer:
                customer.activation_key = code
                customer.key_expiry_date = day
                customer.save()

        # send the user an SMS with the code
        # TODO: Add send sms code
        return Response(
            status=status.HTTP_201_CREATED,
            data={"data": data})


def save_new_shopkeeper(data):
    """Save a new shopkeeper."""
    username = data.get("username" or None)
    first_name = data.get("first_name" or None)
    last_name = data.get("last_name" or None)
    password = data.get("password" or None)
    phonenumber = data.get("phonenumber" or None)
    gender = data.get("gender" or None)
    date_of_birth = data.get("date_of_birth" or None)
    # TODO: get avatar
    user = User.objects.create(
        username=username, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.userprofile.user = user
    user.userprofile.phonenumber = phonenumber
    user.userprofile.gender = gender
    user.userprofile.date_of_birth = datetime.datetime.strptime(
        date_of_birth, "%Y-%m-%d")
    # set shopkeeper as not active, not staff and not superuser
    user.is_active = False
    user.is_staff = False
    user.is_superuser = False
    user.save()
    return user


def save_new_customer(data):
    """Save a new Customer object."""
    shopkeeper_id = data.get("shopkeeper_id" or None)
    first_name = data.get("first_name" or None)
    last_name = data.get("last_name" or None)
    phonenumber = data.get("phonenumber" or None)
    gender = data.get("gender" or None)
    date_of_birth = data.get("date_of_birth" or None)
    try:
        shopkeeper = User.objects.get(id=shopkeeper_id)
        customer = Customer.objects.create(
            owner=shopkeeper.userprofile,
            first_name=first_name,
            last_name=last_name,
            phonenumber=phonenumber,
            gender=gender,
            date_of_birth=date_of_birth,
        )
        return customer
    except Exception as e:
        logger.exception("SHOPKEEPER NOT FOUND: {}".format(str(e)))
        logger.error("SHOPKEEPER NOT FOUND: {}".format(str(e)))
        return None
