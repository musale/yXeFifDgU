"""Common utilities when making tests."""
import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.utils import timezone

from loyalty.apps.sms import models as sms
from loyalty.settings import production as settings
from utils import utilities as utils

TEST_MESSAGE = (
    "It is a long established fact that a reader will be distracted by"
    " the readable content of a page when looking at its layout. The"
    " point of using Lorem Ipsum is that it has a more-or-less normal "
    "distribution of letters, as opposed to using 'Content here,"
    " content here', making it look like readable English."
)

TEST_NUMBERS = "+254705867162,+254722210115,+254712391091"
TEST_NUMBERS_LIST = ["0705867162", "0722210115", "0712391091"]

NOW = timezone.now()


def get_test_userprofile(id, user_type):
    """Return a UserProfile object with the specified id."""
    date_of_birth = datetime.datetime.strptime(
        "1993-01-05", "%Y-%m-%d")
    username = "testeruser{}".format(id)
    user = User.objects.create(
        username=username, first_name="admin", last_name="tester",
        email="testeremail@tests.com")
    user.set_password("wecantest$tuff")
    user.userprofile.user = user
    user.userprofile.user_type = user_type
    user.userprofile.phonenumber = "0705881881"
    user.userprofile.activation_key = "ACKY01"
    user.userprofile.gender = "MALE"
    user.userprofile.date_of_birth = date_of_birth
    user.save()
    return user


def get_test_smsoutbox(sender):
    """Set up a test SMSOutbox."""
    smsoutbox = sms.SMSOutbox.objects.create(
        sender=sender.userprofile,
        senderid=settings.SENDER_ID,
        message=TEST_MESSAGE,
        send_type=sms.SEND_TYPES[0][0]
    )
    return smsoutbox


def get_test_smsrecipient(outbox, number):
    """Set up a test SMSRecipient."""
    recipient = sms.SMSRecipient.objects.create(
        message=outbox,
        number=number,
        status="SUCCESS",
        api_id="TEST_API_ID",
        cost=Decimal(utils.get_message_cost(TEST_MESSAGE))
    )
    return recipient


def get_dlrstatus(recipient):
    """Set up a test DlrStatus."""
    dlrstatus = sms.DlrStatus.objects.create(
        recipient=recipient,
        status="SUCCESS",
        reason="SUCCESS",
        api_time=NOW
    )
    return dlrstatus
