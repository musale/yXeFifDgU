"""Utility functions."""
import datetime
import random
import string
from logging import getLogger

from django.utils import timezone

logger = getLogger(__name__)


def generate_code():
    """Generate a random code."""
    code = "{0}{1}".format(
        str(random.randint(11111, 99999)), random.choice(string.letters))
    day = timezone.localtime(timezone.now()) + datetime.timedelta(days=1)
    return code, day
