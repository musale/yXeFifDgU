"""Test sms app."""
from __future__ import unicode_literals

import datetime

from django.test import TestCase

from loyalty.apps.sms import models as sms
from utils import testing_utils as test_with


class SMSOutboxTest(TestCase):
    """Test SMSOutbox."""

    def setUp(self):
        """Set up an SMSOutbox object."""
        self.sender = test_with.get_test_userprofile(4, "SHOPKEEPER")
        self.smsoutbox = test_with.get_test_smsoutbox(self.sender)

    def test_smsoutbox_is_created(self):
        """Check SMSOutbox created."""
        self.assertTrue(True, isinstance(self.smsoutbox, sms.SMSOutbox))


class SMSRecipientTest(TestCase):
    """Test SMSRecipient."""

    def setUp(self):
        """Set up an SMSOutbox, SMSRecipient objects."""
        self.sender = test_with.get_test_userprofile(5, "SHOPKEEPER")
        self.smsoutbox = test_with.get_test_smsoutbox(self.sender)

    def test_smsoutbox_is_created(self):
        """Check SMSOutbox created."""
        self.assertTrue(True, isinstance(self.smsoutbox, sms.SMSOutbox))

    def test_smsrecipients_are_created(self):
        """Check SMSRecipients are created."""
        for phonenumber in test_with.TEST_NUMBERS_LIST:
            self.recipient = test_with.get_test_smsrecipient(
                self.smsoutbox, phonenumber)
            self.assertTrue(True, isinstance(self.recipient, sms.SMSRecipient))


class DlrStatusTest(TestCase):
    """Test DlrStatus."""

    def setUp(self):
        """Set up an SMSOutbox, SMSRecipient and DlrStatus objects."""
        self.sender = test_with.get_test_userprofile(6, "SHOPKEEPER")
        self.smsoutbox = test_with.get_test_smsoutbox(self.sender)
        self.now = datetime.datetime.now()
        self.recipients = []

    def test_smsoutbox_is_created(self):
        """Check SMSOutbox created."""
        self.assertTrue(True, isinstance(self.smsoutbox, sms.SMSOutbox))

    def test_smsrecipients_are_created(self):
        """Check SMSRecipients are created."""
        for phonenumber in test_with.TEST_NUMBERS_LIST:
            self.recipient = test_with.get_test_smsrecipient(
                self.smsoutbox, phonenumber)
            self.assertTrue(True, isinstance(self.recipient, sms.SMSRecipient))

    def test_dlrstatus_are_created(self):
        """Check DlrStatus are created."""
        for phonenumber in test_with.TEST_NUMBERS_LIST:
            self.recipient = test_with.get_test_smsrecipient(
                self.smsoutbox, phonenumber)
            self.recipients.append(self.recipient)

        for recipient in self.recipients:
            self.dlrstatus = test_with.get_dlrstatus(recipient)
            self.assertTrue(True, isinstance(self.dlrstatus, sms.DlrStatus))
