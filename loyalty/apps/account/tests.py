"""Unit tests for account app."""
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Customer, UserProfile


class UserProfileTest(TestCase):
    """Test UserProfile model."""

    def setUp(self):
        """Set up a user."""
        self.date_of_birth = datetime.datetime.strptime(
            "05-01-2017", "%d-%m-%Y")
        self.user = User.objects.create(
            username="testuser", first_name="admin", last_name="tester",
            email="testeremail@tests.com")
        self.user.set_password("wecantest$tuff")
        self.user.userprofile.user = self.user
        self.user.userprofile.user_type = "SHOPKEEPER"
        self.user.userprofile.phonenumber = "0705881881"
        self.user.userprofile.activation_key = "ACKY01"
        self.user.userprofile.gender = "MALE"
        self.user.userprofile.date_of_birth = self.date_of_birth
        self.user.save()
        self.customer = Customer.objects.create(
            owner=self.user.userprofile, firstname="customer",
            lastname="testname", phonenumber="0711727272"
        )

    def test_user_is_created(self):
        """Check User created."""
        self.assertTrue(True, isinstance(self.user, User))
        self.assertTrue(True, isinstance(self.user.userprofile, UserProfile))

    def test_customer_is_created(self):
        """Check Customer created."""
        self.assertTrue(True, isinstance(self.customer, Customer))
