"""Test the api endpoints on /v1/ ."""
from __future__ import unicode_literals

import json
from logging import getLogger

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
        self.payload_shopkeeper = {
            "first_name": "John", "last_name": "Doe", "username": "testuser",
            "user_type": "SHOPKEEPER", "phonenumber": "0705867162",
            "gender": "MALE", "date_of_birth":  "05-01-1993"}

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
        """Test signing up a shopkeper."""
        request = self.factory.post(
            "/v1/account/signup/", json.dumps(self.payload_shopkeeper),
            content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.data.get("data"), self.payload_shopkeeper)
