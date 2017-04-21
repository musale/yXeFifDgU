"""Test billing app."""
from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.test import TestCase

from loyalty.apps.billing.models import CashTransaction
from utils.testing_utils import get_test_userprofile


class CashTransactionTest(TestCase):
    """TestCase for CashTransaction."""

    def setUp(self):
        """Set up a transaction."""
        self.date_of_birth = datetime.datetime.strptime(
            "1993-01-05", "%Y-%m-%d")
        self.amount = Decimal("100")
        self.user = get_test_userprofile(3, "SHOPKEEPER")
        self.transaction = CashTransaction.objects.create(
            user=self.user.userprofile,
            ipn_log_id="RANDOM",
            trans_amount=self.amount
        )

    def test_invalid_cashtransaction(self):
        """Test None cannot be used in CashTransaction."""
        self.transaction.trans_type = None
        self.error = "billing_cashtransaction.trans_type may not be NULL"
        with self.assertRaises(Exception) as context:
            self.transaction.save()
        self.assertTrue(self.error in context.exception)

    def test_valid_cashtransaction(self):
        """Test a valid cash transaction."""
        self.transaction.trans_type = "MPESA_TOPUP"
        self.transaction.save()
        self.assertTrue(True, isinstance(self.transaction, CashTransaction))
