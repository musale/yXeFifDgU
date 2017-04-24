"""Unit tests for account app."""
from __future__ import unicode_literals

from django.test import TestCase

from loyalty.settings import production as setting
from utils import send_sms as sms
from utils import testing_utils as test_with
from utils.AfricasTalkingGateway import AfricasTalkingGateway


class SendUserSMSTest(TestCase):
    """Test SendUserSMS object."""

    def setUp(self):
        """Set it up."""
        self.sender = test_with.get_test_userprofile(7,  "SHOPKEEPER")
        self.outbox = sms.SendUserSMS(
            to=test_with.TEST_NUMBERS_LIST, message=test_with.TEST_MESSAGE,
            senderid=setting.SENDER_ID, sender=self.sender)

    def test_message_gateway(self):
        """Test the AfricasTalkingGateway."""
        gateway = self.outbox.message_gateway()
        self.assertTrue(gateway, isinstance(gateway, AfricasTalkingGateway))
        self.assertEqual("DukaConnect", "DukaConnect")

    def test_prepare_phone_numbers(self):
        """Test prepare_phone_numbers()."""
        phone_numbers, _ = self.outbox.prepare_phone_numbers()
        self.assertTrue(self.outbox.to, isinstance(self.outbox.to, list))
        self.assertEqual(test_with.TEST_NUMBERS, phone_numbers)
        self.assertTrue(phone_numbers, isinstance(phone_numbers, str))

    def test_check_message_cost(self):
        """Test check_message_cost()."""
        self.assertTrue(self.outbox.check_message_cost()["error"])
