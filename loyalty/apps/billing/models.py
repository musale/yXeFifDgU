"""Billing tables."""
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from loyalty.apps.account.models import UserProfile

TRANSACTION_TYPES = (
    (None, 'CHOOSE A TYPE'),
    ('TRIAL_CREDIT', 'TRIAL_CREDIT'),
    ('CASH_TOPUP', 'CASH_TOPUP'),
    ('MPESA_TOPUP', 'MPESA_TOPUP'),
    ('PAYPAL_TOPUP', 'PAYPAL_TOPUP'),
    ('CHEQUE_TOPUP', 'CHEQUE_TOPUP'),
    ('EFT_TOPUP', 'EFT_TOPUP'),
    ('CASH_REFUND', 'CASH_REFUND'),
    ('SAMBAZA_IN', 'SAMBAZA_IN'),
    ('SAMBAZA_OUT', 'SAMBAZA_OUT'),
    ('REFERRAL_CREDIT', 'REFERRAL_CREDIT'),
    ('OUTGOING_MESSAGE', 'OUTGOING_MESSAGE'),
    ('SCHEDULER_RESERVE', 'SCHEDULER_RESERVE'),
    ('RESERVE_REFUND', 'RESERVE_REFUND'),
    ('INCOMING_REPLY', 'INCOMING_REPLY'),
)


class CashTransaction(models.Model):
    """Cash transactions done by user."""

    user = models.ForeignKey(UserProfile)
    trans_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    ipn_log_id = models.CharField(max_length=32)
    trans_amount = models.DecimalField(max_digits=10, decimal_places=2)
    trans_currency = models.CharField(max_length=8, default='KES')
    trans_date = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        """Override save method."""
        if not self.trans_date:
            self.trans_date = timezone.now()
        super(CashTransaction, self).save()

    def __str__(self):
        """Format object display."""
        display = "{0}-{1} {2}".format(
            self.trans_type, self.trans_currency, self.trans_amount)
        return display

    def readable_name(self):
        """Readable name."""
        return self.trans_type.replace('_', ' ').title()
