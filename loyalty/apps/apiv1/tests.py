"""Test the api endpoints on /v1/ ."""
from __future__ import unicode_literals

import datetime
import json
from logging import getLogger

from django.contrib.auth.models import User
# from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from loyalty.apps.apiv1.views import SignUpApiView

# TODO: test SignUpApiView
logger = getLogger(__name__)


class SignUpApiViewTest(APITestCase):
    """Unit test the SignUpApiView."""

    def setUp(self):
        """Set up request."""
        self.factory = APIRequestFactory()
        self.view = SignUpApiView.as_view()
        self.date_of_birth = datetime.datetime.strptime(
            "05-01-2017", "%d-%m-%Y")
        self.shopkeeper = User.objects.create(
            username="testuser2", first_name="admin", last_name="tester",
            email="testeremail@tests.com")
        self.shopkeeper.set_password("wecantest$tuff")
        self.shopkeeper.userprofile.user = self.shopkeeper
        self.shopkeeper.userprofile.user_type = "SHOPKEEPER"
        self.shopkeeper.userprofile.phonenumber = "0705881881"
        self.shopkeeper.userprofile.activation_key = "ACKY01"
        self.shopkeeper.userprofile.gender = "MALE"
        self.shopkeeper.userprofile.date_of_birth = self.date_of_birth
        self.shopkeeper.save()
        self.payload_shopkeeper = {
            "first_name": "John", "last_name": "Doe", "username": "testuser",
            "user_type": "SHOPKEEPER", "phonenumber": "0705867162",
            "gender": "MALE", "date_of_birth":  "05-01-1993"}
        self.payload_customer = {
            "first_name": "John", "last_name": "Doe", "user_type": "CUSTOMER",
            "phonenumber": "0705867162", "gender": "MALE",
            "date_of_birth":  "05-01-1993",
            "shopkeeper_id": self.shopkeeper.id}

    def test_account_signup_endpoint(self):
        """Test the endpoint GET /v1/account/signup/ ."""
        self.test_get = self.client.get("/v1/account/signup/")
        self.test_post = self.client.post(
            "/v1/account/signup/", self.payload_shopkeeper, format="json")
        # status_code=405 means Method is not allowed
        self.assertEqual(405, self.test_get.status_code)
        # status_code=200 means OK
        self.assertEqual(
            201, self.test_post.status_code)

    def test_signingup_shopkeeper(self):
        """Test signing up a shopkeeper."""
        request = self.factory.post(
            "/v1/account/signup/", json.dumps(self.payload_shopkeeper),
            content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.data.get("data"), self.payload_shopkeeper)

    def test_signingup_customer(self):
        """Test signing up a customer."""
        request = self.factory.post(
            "/v1/account/signup/", json.dumps(self.payload_customer),
            content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.data.get("data"), self.payload_customer)
