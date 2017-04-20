"""Test the api endpoints on /v1/ ."""
from __future__ import unicode_literals

from logging import getLogger

from rest_framework import status
from rest_framework.test import APIClient, APITestCase, CoreAPIClient

# TODO: test SignUpApiView
logger = getLogger(__name__)


class SignUpApiViewTest(APITestCase):
    """Unit test the SignUpApiView."""

    def setUp(self):
        """Set up request."""
        self.client = APIClient()
        self.payload = {
            "first_name": "John", "last_name": "Doe", "username": "testuser",
            "user_type": "SHOPKEEPER", "phonenumber": "0705867162",
            "gender": "MALE", "avatar": "asjadkjsdkj"}

    def test_account_signup_endpoint(self):
        """Test the endpoint GET /v1/account/signup/ ."""
        self.test_get = self.client.get("/v1/account/signup/")
        self.test_post = self.client.post(
            "/v1/account/signup/", self.payload, format="json")
        # status_code=405 means Method is not allowed
        self.assertEqual(405, self.test_get.status_code)
        # status_code=200 means OK
        self.assertEqual(
            200, self.test_post.status_code)

    def test_signingup_shopkeeper(self):
        """Test signing up a shopkeper."""
        client = CoreAPIClient()
        self.signup = client.post(
            "/v1/account/signup/", self.payload, format="json")
        data = self.signup
        # user_type = data.get("user_type" or None)
        logger.info("data: {}".format(data))
        # logger.info("user_type{}".format(user_type))
        self.assertEqual(
            200, self.test_post.status_code)
