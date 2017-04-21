"""Object holder for all SMS."""
from __future__ import unicode_literals

from django.db import models

from loyalty.apps.account.models import UserProfile
from loyalty.apps.billing.models import CashTransaction

SEND_TYPES = (
    ("NORMAL_SMS", "NORMAL_SMS"),
    ("CUSTOM_SMS", "CUSTOM_SMS"),
    ("AUTO_RESP", "AUTO_RESP"),
)


class SMSOutbox(models.Model):
    """Outbox SMS table."""

    sender = models.ForeignKey(UserProfile, related_name="sender")
    senderid = models.CharField(max_length=20)
    message = models.TextField()
    currency = models.CharField(max_length=5, default="KES")
    reply_code = models.CharField(max_length=10, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    send_type = models.CharField(max_length=20, choices=SEND_TYPES)
    public = models.BooleanField(default=False)

    class Meta:
        """Meta data class."""

        ordering = ["-id"]

    def message_cost(self):
        """SMS COST."""
        return self.smsrecipient_set.aggregate(
            models.Sum("cost"))["cost__sum"] or 0.00

    def trans_cost(self):
        """Transaction cost."""
        try:
            cost = CashTransaction.objects.values_list(
                "trans_amount", flat=True).get(ipn_log_id=self.pk)
        except CashTransaction.MultipleObjectsReturned:
            trans = CashTransaction.objects.filter(ipn_log_id=self.pk)
            amount = [t.trans_amount for t in trans]
            cost = float(sum(amount))
        return cost

    def processing(self):
        """SMS with PROCESSING status."""
        return self.smsrecipient_set.filter(status="PROCESSING").count()

    def success(self):
        """SMS with SUCCESS status."""
        return self.smsrecipient_set.filter(status="SENT").count() + \
            self.smsrecipient_set.filter(status="SUCCESS").count()

    def failed(self):
        """SMS with FAILED status."""
        return self.smsrecipient_set.filter(status="FAILED").count()

    def invalid_num(self):
        """SMS with INVALID_NUMBER status."""
        return self.smsrecipient_set.filter(status="INVALID_NUM").count()

    def opt_out(self):
        """SMS with OPTED_OUT status."""
        return self.smsrecipient_set.filter(status="OPTED_OUT").count()

    def recipient_count(self):
        """View this sms recipients count."""
        return self.smsrecipient_set.count()

    def recipients(self):
        """View this sms recipients."""
        return self.smsrecipient_set.all()


class SMSRecipient(models.Model):
    """SMS recipient table."""

    message = models.ForeignKey(SMSOutbox)
    number = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    api_id = models.CharField(max_length=64, null=True, default=None)
    reason = models.CharField(max_length=200, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default="KES")

    class Meta:
        """Metadata class."""

        ordering = ["-id"]


class DlrStatus(models.Model):
    """Delivery Status of a message."""

    recipient = models.OneToOneField(SMSRecipient)
    status = models.CharField(max_length=20)
    reason = models.CharField(max_length=50)
    api_time = models.DateTimeField(null=True)

    class Meta:
        """Metadata class."""

        ordering = ["-id"]
