"""Utility functions."""
import datetime
import math
import random
import string
from logging import getLogger

from django.utils import timezone

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
