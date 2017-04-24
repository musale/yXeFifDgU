"""Utility functions."""
import datetime
import math
import random
import re
import string
from logging import getLogger

from django.db.models import Sum
from django.utils import timezone

from loyalty.apps.billing import models as bill
from utils import config

logger = getLogger(__name__)
CHARACTER_COUNT = config.SMS_UTILS["character_count"]
DEFAULT_COST = config.SMS_UTILS["default_cost"]


def generate_code():
    """Generate a random code."""
    code = "{0}{1}".format(
        str(random.randint(11111, 99999)), random.choice(string.letters))
    day = timezone.localtime(timezone.now()) + datetime.timedelta(days=1)
    return code, day


def get_message_cost(message):
    """Get the cost of a single message."""
    pages = int(math.ceil(float(len(message)) / CHARACTER_COUNT))
    return DEFAULT_COST * pages


def is_kenyan(number, standard=None):
    """Validate a kenyan number."""
    pattern = re.compile(r'^[7]{1}[0-9]{8}$')
    bad_ones = ['\t', '\n', ' ', ',', '-', '(', ')', '.', "'", '"']
    number = str(number)
    if not number or len(number) < 2:
        return False
    for x in bad_ones:
        number = number.replace(x, '')

    if number[0] == '+' or number[0] == '0':
        number = number[1:]
    if number[0:3] == '254':
        number = number[3:]
    if len(number) < 9:
        return False
    if number[0] == '0':
        number = number[1:]
    if not pattern.match(number):
        return False
    validated_number = '+254%s' % (number,)
    if standard:
        validated_number = '%s%s' % (standard, number)
    return validated_number


def get_user_balance(user):
    """Get a user balance."""
    balance = 0.0
    trans = bill.CashTransaction.objects.filter(
        user=user.userprofile).aggregate(amount=Sum('trans_amount'))
    if trans['amount']:
        balance = float(trans['amount'])
    return balance
