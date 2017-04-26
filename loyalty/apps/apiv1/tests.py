"""Test the api endpoints on /v1/ ."""
from __future__ import unicode_literals

import datetime
import json
from logging import getLogger

from rest_framework.test import APIRequestFactory, APITestCase

from loyalty.apps.apiv1.views import (SignUpCustomerApiView,
                                      SignUpShopkeeperApiView,
                                      VerifyShopkeeperApiView)
from utils.testing_utils import get_test_userprofile

logger = getLogger(__name__)


class SignUpApiViewTest(APITestCase):
    """Unit test the SignUpApiView."""

    def setUp(self):
        """Set up request."""
        self.factory = APIRequestFactory()
        self.shopkeeper_view = SignUpShopkeeperApiView.as_view()
        self.customer_view = SignUpCustomerApiView.as_view()
        self.date_of_birth = datetime.datetime.strptime(
            "1993-01-05", "%Y-%m-%d")
        self.shopkeeper = get_test_userprofile(2, "SHOPKEEPER")
        self.payload_shopkeeper = {
            "first_name": "John", "last_name": "Doe", "username": "testuser",
            "user_type": "SHOPKEEPER", "phonenumber": "0705867162",
            "gender": "MALE", "date_of_birth":  "1993-01-05"}
        self.payload_customer = {
            "first_name": "John", "last_name": "Doe", "user_type": "CUSTOMER",
            "phonenumber": "0705867162", "gender": "MALE",
            "date_of_birth":   "1993-01-05",
            "shopkeeper_id": self.shopkeeper.id}

    def test_accounts_signup_shopkeeper_endpoint(self):
        """Test the endpoint GET /v1/accounts/signup/shopkeepers/ ."""
        self.test_get = self.client.get("/v1/accounts/signup/shopkeepers/")
        self.test_post = self.client.post(
            "/v1/accounts/signup/shopkeepers/",
            self.payload_shopkeeper, format="json")
        # status_code=405 means Method is not allowed
        self.assertEqual(405, self.test_get.status_code)
        # status_code=200 means OK
        self.assertEqual(
            201, self.test_post.status_code)

    def test_accounts_signup_customer_endpoint(self):
        """Test the endpoint GET /v1/accounts/signup/customers/ ."""
        self.test_get = self.client.get("/v1/accounts/signup/customers/")
        self.test_post = self.client.post(
            "/v1/accounts/signup/customers/",
            self.payload_customer, format="json")
        # status_code=405 means Method is not allowed
        self.assertEqual(405, self.test_get.status_code)
        # status_code=200 means OK
        self.assertEqual(
            201, self.test_post.status_code)

    def test_signingup_shopkeeper(self):
        """Test signing up a shopkeeper."""
        request = self.factory.post(
            "/v1/accounts/signup/shopkeepers/",
            json.dumps(self.payload_shopkeeper),
            content_type='application/json')
        response = self.shopkeeper_view(request)
        self.assertEqual(response.data.get("data"), self.payload_shopkeeper)

    def test_signingup_customer(self):
        """Test signing up a customer."""
        request = self.factory.post(
            "/v1/accounts/signup/customers/",
            json.dumps(self.payload_customer),
            content_type='application/json')
        response = self.customer_view(request)
        self.assertEqual(response.data.get("data"), self.payload_customer)


class VerifyShopkeeperApiViewTest(APITestCase):
    """Test VerifyCustomerApiView."""

    def setUp(self):
        """Setup default vars."""
        self.url = "/v1/accounts/verify/shopkeepers/"
        self.user = get_test_userprofile(8, "SHOPKEEPER")
        self.payload = {
            "userCode": self.user.userprofile.activation_key,
            "userType": "SHOPKEEPER"
        }
        self.view = VerifyShopkeeperApiView.as_view()

    def test_accounts_verify_shopkeeper_endpoint(self):
        """Test the endpoint /v1/accounts/verify/shopkeepers/ exists."""
        self.test_get = self.client.get(self.url)
        self.test_post = self.client.post(
            self.url, self.payload, format="json")
        self.assertEqual(405, self.test_get.status_code)
        self.assertEqual(202, self.test_post.status_code)

    def test_wrong_verify_code(self):
        """Test the userCode provided DOES NOT exists."""
        payload = {
            "userCode": "WRONGC0DE",
            "userType": "SHOPKEEPER"
        }
        self.test_post = self.client.post(self.url, payload, format="json")
        self.assertEqual(404, self.test_post.status_code)

    def test_right_verify_code(self):
        """Test the userCode provided exists."""
        self.test_post = self.client.post(
            self.url, self.payload, format="json")
        self.assertEqual(
            self.test_post.data["userCode"], self.payload["userCode"])
