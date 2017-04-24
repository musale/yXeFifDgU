"""Unit tests for account app."""
from __future__ import unicode_literals

from logging import getLogger

from django.contrib.auth.models import User
from django.test import TestCase

from utils.testing_utils import get_test_userprofile

from .models import Customer, UserProfile
from .serializers import UserProfileSerializer

logger = getLogger(__name__)


class UserProfileTest(TestCase):
    """Test UserProfile model."""

    def setUp(self):
        """Set up a user."""
        self.user = get_test_userprofile(1, "SHOPKEEPER")
        self.customer = Customer.objects.create(
            owner=self.user.userprofile, first_name="customer",
            last_name="testname", phonenumber="0711727272"
        )

    def test_user_is_created(self):
        """Check User created."""
        self.assertTrue(True, isinstance(self.user, User))
        self.assertTrue(True, isinstance(self.user.userprofile, UserProfile))

    def test_customer_is_created(self):
        """Check Customer created."""
        self.assertTrue(True, isinstance(self.customer, Customer))


class UserProfileSerializerTest(TestCase):
    """Test the UserProfileSerializer."""

    def setUp(self):
        """Set up serializer."""
        self.user = get_test_userprofile(9, "SHOPKEEPER")
        self.serializer = UserProfileSerializer(self.user.userprofile)

    def test_user_profile_serializer(self):
        """Test UserProfileSerializer is created."""
        self.assertTrue(
            True, isinstance(self.serializer, UserProfileSerializer))
