"""Sending SMS functionality."""
from rest_framework import status
from rest_framework.response import Response

from loyalty.apps.billing import models as billing
from loyalty.apps.sms import models as sms
from loyalty.settings import production as setting
from utils import utilities
from utils.AfricasTalkingGateway import AfricasTalkingGateway


class SendUserSMS(object):
    """SendUserSMS."""

    def __init__(self, to, message, senderid, sender):
        """Initialize with the SMSOutbox object."""
        super(SendUserSMS, self).__init__()
        self.to = to
        self.message = message
        self.senderid = senderid
        self.sender = sender
        self.message_cost = utilities.get_message_cost(self.message)
        self.user_balance = utilities.get_user_balance(self.sender)

    def message_gateway(self):
        """Get the gateway."""
        gateway = get_gateway()
        return gateway

    def prepare_phone_numbers(self):
        """Transform a list of numbers to a string of numbers."""
        return get_phone_numbers(self.to)

    def check_message_cost(self):
        """Check the message cost and return error if low."""
        _, valid_numbers = self.prepare_phone_numbers()
        total_cost = len(valid_numbers) * self.message_cost

        if total_cost > self.user_balance:
            return {
                "error": True,
                "data": "You need additional KES {0} to send the SMS".format(
                    total_cost - self.user_balance
                )
            }
        else:
            return {
                "error": False,
                "data": "Message sent"
            }

    def save_outbox_message(self):
        """Save to SMSOutbox."""
        outboxMessage = sms.SMSOutbox(
            sender=self.sender.userprofile,
            senderid=self.senderid,
            message=self.message,
            send_type="NORMAL_SMS"
        )
        outboxMessage.save()
        return outboxMessage

    def save_sms_recipient(self, response, outboxMessage):
        """Save SMS recipients."""
        message_cost = 0.0
        for result in response:
            cost = self.message_cost
            if result["status"] == "Success":
                recipient = sms.SMSRecipient(
                    message=outboxMessage,
                    number=result["number"],
                    status="SENT",
                    api_id=result["messageId"],
                    reason=None,
                    cost=cost
                )
                recipient.save()
                message_cost += cost
            else:
                if result["status"] == "Invalid Phone Number":
                    status_ = "INVALID_NUM"
                else:
                    status_ = result["status"]
                recipient = sms.SMSRecipient(
                    message=outboxMessage,
                    number=result["number"],
                    status=status_,
                    api_id=result["messageId"],
                    reason=None,
                    cost=cost
                )
                recipient.save()

        return message_cost

    def send_message(self, phone_numbers):
        """Send an SMS given a string of prepare_phone_numbers."""
        gateway = self.message_gateway()
        response = gateway.sendMessage(
            to_=phone_numbers, message_=self.message, from_=self.senderid)
        # Initialize cost
        outboxMessage = self.save_outbox_message()
        message_cost = self.save_sms_recipient(response, outboxMessage)

        # deduct user amount
        cashTransaction = billing.CashTransaction(
            user=self.sender.userprofile,
            trans_type="OUTGOING_MESSAGE",
            ipn_log_id=outboxMessage.pk,
            trans_amount=float(message_cost) * -1
        )
        cashTransaction.save()
        response[0]["cost"] = message_cost
        return Response(
            {"Success": "Message Sent", "response": response},
            status=status.HTTP_200_OK
        )


def send_out_message(to, message, senderid, sender=None):
    """Global send a message."""
    if sender:
        outbox = SendUserSMS(
            to=to, message=message, senderid=senderid, sender=sender)
        phone_numbers, _ = outbox.prepare_phone_numbers()
        cost = outbox.check_message_cost()
        if cost["error"]:
            # low balance
            return Response(data=cost, status=status.HTTP_200_OK)
        else:
            return outbox.send_message(phone_numbers)
    else:
        gateway = get_gateway()
        phone_numbers, _ = get_phone_numbers(to)
        response = gateway.sendMessage(
            to_=phone_numbers, message_=message, from_=senderid)
        return Response(
            {"Success": "Message Sent", "response": response},
            status=status.HTTP_200_OK
        )


def get_gateway():
    """Get the gateway."""
    if setting.DEBUG:
        gateway = AfricasTalkingGateway(
            setting.AFRICAS_TALKING_USERNAME,
            setting.AFRICAS_TALKING_API_KEY, "sandbox")
    else:
        gateway = AfricasTalkingGateway(
            setting.AFRICAS_TALKING_USERNAME,
            setting.AFRICAS_TALKING_API_KEY)
    return gateway


def get_phone_numbers(phone_numbers_list):
    """Transform a list of numbers to a string of numbers."""
    valid_numbers = []
    for number in phone_numbers_list:
        valid = utilities.is_kenyan(number)
        if valid:
            valid_numbers.append(valid)
    phone_numbers = ",".join(valid_numbers)
    return phone_numbers, valid_numbers
