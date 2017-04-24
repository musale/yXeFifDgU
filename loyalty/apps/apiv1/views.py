"""API version 1 for dukaconnect loyalty."""
from __future__ import unicode_literals

import datetime
# from django.http import Http404
from logging import getLogger

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from loyalty.apps.account.models import Customer, UserProfile
from loyalty.apps.account.serializers import UserProfileSerializer
from loyalty.settings import production as setting
from rest_framework_jwt.settings import api_settings
from utils.send_sms import (VERIFICATION_SMS, WELCOME_CUSTOMER_SMS,
                            send_out_message)
from utils.utilities import generate_code

logger = getLogger(__name__)
NOW = timezone.now()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@permission_classes((AllowAny, ))
class SignUpShopkeeperApiView(APIView):
    """Sign up a shopkeeper."""

    http_method_names = ['post']
    # generate new code and expiry date for the shopkeeper
    code, day = generate_code()

    def post(self, request, format=None):
        """Handle POST account/signup/ ."""
        data = request.data
        user_type = data.get("user_type" or None)
        phonenumber = data.get("phonenumber" or None)
        if user_type == "SHOPKEEPER":
            user = save_new_shopkeeper(data)
            # save shopkeeper
            user.userprofile.user_type = user_type
            # save the code and expiry date
            user.userprofile.activation_key = self.code
            user.userprofile.key_expiry_date = self.day
            user.save()
            message = VERIFICATION_SMS.format(user.get_full_name(), self.code)
            send_out_message(
                [phonenumber], message, setting.SENDER_ID, sender=user)
        return Response(
            status=status.HTTP_201_CREATED,
            data={"data": data})


@permission_classes((AllowAny, ))
class SignUpCustomerApiView(APIView):
    """Sign up a shopkeeper or a customer."""

    http_method_names = ['post']
    code, day = generate_code()

    def post(self, request, format=None):
        """Handle POST account/signup/ ."""
        data = request.data
        user_type = data.get("user_type" or None)
        phonenumber = data.get("phonenumber" or None)
        if user_type == "CUSTOMER":
            # save a customer
            customer = save_new_customer(data)
            if customer:
                customer.activation_key = self.code
                customer.key_expiry_date = self.day
                customer.save()
                # send welcome sms to shopkeepers
                message = WELCOME_CUSTOMER_SMS.format(customer.get_full_name())
                send_out_message([phonenumber], message, setting.SENDER_ID)
        return Response(
            status=status.HTTP_201_CREATED,
            data={"data": data})


@permission_classes((AllowAny, ))
class VerifyCustomerApiView(APIView):
    """Verify a customer given an activation_key."""

    http_method_names = ['post']

    def post(self, request, format=None):
        """Handle POST accounts/verify/shopkeepers ."""
        data = request.data
        user_type = data.get("userType" or None)
        code = data.get("userCode" or None)
        if user_type == "SHOPKEEPER":
            try:
                shopkeeper = UserProfile.objects.get(activation_key=code)
                return verify_shopkeeper(shopkeeper)
            except Exception as e:
                logger.error(
                    "SHOPKEEPER WITH CODE {} DOES NOT EXIST".format(code))
                logger.exception(
                    "ERROR GETTING SHOPKEEPER: {}".format(str(e)))
                return Response(status=status.HTTP_404_NOT_FOUND, data={
                    "error": True,
                    "message": (
                        "Shopkeeper with code {}"
                        " does not exist.".format(code)
                    ),
                    "userCode": code
                })


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


def verify_shopkeeper(shopkeeper):
    """Verify a shopkeeper fetched with a given code."""
    serializer = UserProfileSerializer(shopkeeper.user.userprofile)
    userCode = shopkeeper.activation_key
    if shopkeeper.key_expiry_date < NOW:
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={
            "error": True,
            "message": (
                "The code {} has expired. Generate a new one to verify".format(
                    userCode)
            ),
            "userCode": userCode
        })
    else:
        shopkeeper.user.is_active = True
        shopkeeper.save()
        payload = jwt_payload_handler(shopkeeper.user)
        token = jwt_encode_handler(payload)
        data = {
            "token": token,
            "userData": serializer.data,
            "error": False,
            "message": (
                "Login success. {} welcome to DukaConnect.".format(
                    shopkeeper.user.get_full_name())
            ),
            "userCode": userCode}
        return Response(status=status.HTTP_202_ACCEPTED, data=data)
