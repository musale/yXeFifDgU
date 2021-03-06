"""Configuration file."""

import os
from socket import gethostname

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get environment variables."""
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(
            "Set the %s environment variable" % var_name)


def getDebug():
    """Get the DEBUG value."""
    if get_env_variable(
        "DUKA_ENV") == "production" or get_env_variable(
            "DUKA_ENV") == "development":
        return True
    else:
        return False


RAVEN_DNS = "%s:%s@sentry.io/%s" % (get_env_variable("RAVEN_CODE_ONE"),
                                    get_env_variable("RAVEN_CODE_TWO"),
                                    get_env_variable("RAVEN_PORT"))


# Database settings
DB = {
    "name": get_env_variable("LOYALTY_DB_NAME"),
    "host": get_env_variable("LOYALTY_DB_HOST"),
    "user": get_env_variable("LOYALTY_DB_USER"),
    "password": get_env_variable("LOYALTY_DB_PASSWORD"),
    "port": get_env_variable("LOYALTY_DB_PORT"),
}


# Django settings
DJANGO = {
    "secret_key": "mvm-ffhmu7)2)8=_zi7o6(5a8#2sdf!)se^0r6e-ktq+j",
    "debug": getDebug(),
    "allowed_hosts": ["loyalty.dukaconnect.com", "dev.loyalty.com"],
    "ip": "139.162.189.163" if gethostname() == "apps0" else "192.168.33.17",
    "log_file": get_env_variable("LOG_FILE"),
    "static_url": "/static/",
    "static_root": "/apps/loyalty/static/",
    "media_url": "/media/",
    "media_root": "/apps/loyalty/media/",
}

# Email settings
EMAIL = {
    "email": "jambo@dukaconnect.com",
    "password": get_env_variable("EMAIL_PASSWORD"),
    "host": "smtp.gmail.com", "port": 587,
    "default": "DUKAConnect <jambo@dukaconnect.com>"
}


def getAftApiCredentials():
    """Get the AfricasTalking api credentials for local and live."""
    if getDebug():
        # local
        return {
            "user": get_env_variable("AT_API_USER"),
            "key": get_env_variable("AT_API_KEY_STAGE"),
            "senderid": "50012"
        }
    else:
        # production settings
        return {
            "user": get_env_variable("AT_API_USER"),
            "key": get_env_variable("AT_API_KEY_PROD"),
            "senderid": get_env_variable("SENDER_ID")
        }


AFT_API = getAftApiCredentials()

VERIFY = "Hi %s, welcome to DukaConnect. Use %s to verify your account."

VERIFY_RESET_PASSWORD = "Hi %s, use %s to verify your password reset request."

SMS_UTILS = {
    "default_cost": 5.0,
    "character_count": 160,
    "verify_account_text": VERIFY,
    "verify_reset_password": VERIFY_RESET_PASSWORD
}
