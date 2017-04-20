"""API version 1 for dukaconnect loyalty."""
from __future__ import unicode_literals

# from django.http import Http404
from logging import getLogger

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.utilities import generate_code

logger = getLogger(__name__)


@permission_classes((AllowAny, ))
class SignUpApiView(APIView):
    """Sign up a shopkeeper or a customer."""

    http_method_names = ['post']

    def post(self, request, format=None):
        """Handle POST account/signup/ ."""
        data = request.POST
        user_type = data.get("user_type" or None)
        if user_type == "SHOPKEEPER":
            user = save_new_shopkeeper(data)
            # generate new code and expiry date for the shopkeeper
            code, day = generate_code()
            # save the code and expiry date
            user.userprofile.activation_key = code
            user.userprofile.key_expiry_date = day

            user.save()

            # send the user an SMS with the code
            # TODO: Add send sms code
            return Response(status=status.HTTP_201_CREATED)
        elif user_type == "CUSTOMER":
            # TODO: save a customer
            pass
            return Response(status=status.HTTP_202_ACCEPTED)


def save_new_shopkeeper(data):
    """Save a new shopkeeper."""
    username = data.get("username" or None)
    first_name = data.get("first_name" or None)
    last_name = data.get("last_name" or None)
    user_type = data.get("user_type" or None)
    password = data.get("password" or None)
    phonenumber = data.get("phonenumber" or None)
    gender = data.get("gender" or None)
    date_of_birth = data.get("date_of_birth" or None)
    # TODO: get avatar
    user = User.objects.create(
        username=username, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.userprofile.user = user
    user.userprofile.user_type = user_type
    user.userprofile.phonenumber = phonenumber
    user.userprofile.gender = gender
    user.userprofile.date_of_birth = date_of_birth
    # set shopkeeper as not active, not staff and not superuser
    user.is_active = False
    user.is_staff = False
    user.is_superuser = False
    return user.save()
