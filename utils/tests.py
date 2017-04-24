"""Unit tests for account app."""
from __future__ import unicode_literals

from django.test import TestCase

from loyalty.apps.sms import models as smsobj
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
        self.phone_numbers, _ = self.outbox.prepare_phone_numbers()
        self.outboxMessage = self.outbox.save_outbox_message()

    def test_message_gateway(self):
        """Test the AfricasTalkingGateway."""
        gateway = self.outbox.message_gateway()
        self.assertTrue(gateway, isinstance(gateway, AfricasTalkingGateway))
        self.assertEqual("DukaConnect", "DukaConnect")

    def test_prepare_phone_numbers(self):
        """Test prepare_phone_numbers()."""
        self.assertTrue(self.outbox.to, isinstance(self.outbox.to, list))
        self.assertEqual(test_with.TEST_NUMBERS, self.phone_numbers)
        self.assertTrue(
            self.phone_numbers, isinstance(self.phone_numbers, str))

    def test_check_message_cost(self):
        """Test check_message_cost()."""
        self.assertTrue(self.outbox.check_message_cost()["error"])

    def test_send_message(self):
        """Test sending an sms."""
        response = self.outbox.send_message(self.phone_numbers)
        self.assertEqual(200, response.status_code)

    def test_save_outbox_message(self):
        """Test saving a message in outbox."""
        self.assertTrue(
            self.outboxMessage,
            isinstance(self.outboxMessage, smsobj.SMSOutbox))

    def test_save_sms_recipient(self):
        """Test saving the SMS recipients."""
        gateway = self.outbox.message_gateway()
        response = gateway.sendMessage(
            to_=self.phone_numbers, message_=test_with.TEST_MESSAGE,
            from_=setting.SENDER_ID)
        message_cost = self.outbox.save_sms_recipient(
            response, self.outboxMessage)
        self.assertTrue(message_cost, isinstance(message_cost, float))
