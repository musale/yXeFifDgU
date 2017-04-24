"""Sending SMS functionality."""
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

    def message_gateway(self):
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

    def prepare_phone_numbers(self):
        """Transform a list of numbers to a string of numbers."""
        # validate phone_numbers
        valid_numbers = []
        for number in self.to:
            valid = utilities.is_kenyan(number)
            if valid:
                valid_numbers.append(valid)
        phone_numbers = ','.join(valid_numbers)
        return phone_numbers, valid_numbers

    def check_message_cost(self):
        """Check the message cost and return error if low."""
        # check message cost
        message_cost = utilities.get_message_cost(self.message)
        user_balance = utilities.get_user_balance(self.sender)
        _, valid_numbers = self.prepare_phone_numbers()
        total_cost = len(valid_numbers) * message_cost

        if total_cost > user_balance:
            return {
                "error": True,
                "data": "You need additional KES {0} to send the SMS".format(
                    total_cost - user_balance
                )
            }
        else:
            return {
                "error": False,
                "data": "Message sent"
            }
