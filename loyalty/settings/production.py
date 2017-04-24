"""Django settings for loyalty project."""

import os
import sys

# import raven
from utils.config import AFT_API, DB, DJANGO, EMAIL, RAVEN_DNS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(BASE_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = DJANGO['allowed_hosts']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'loyalty.apps.account',
    'loyalty.apps.administrator',
    'loyalty.apps.apiv1',
    'loyalty.apps.billing',
    'loyalty.apps.customer',
    'loyalty.apps.point',
    'loyalty.apps.purchase',
    'loyalty.apps.shopkeeper',
    'loyalty.apps.sms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'loyalty.urls'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'loyalty.wsgi.application'


# Database: Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB['name'],
        'USER': DB['user'],
        'PASSWORD': DB['password'],
        'HOST': DB['host'],
        'PORT': DB['port'],
    }
}
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

# Sentry
RAVEN_CONFIG = {
    'dsn': "https://" + RAVEN_DNS,
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL['host']
EMAIL_HOST_USER = EMAIL['email']  # gmail username
EMAIL_HOST_PASSWORD = EMAIL['password']  # gmail password
EMAIL_PORT = EMAIL['port']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL['default']
SERVER_EMAIL = EMAIL['email']

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        ),
    },
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s]" +
            " %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            # To capture more than ERROR, change to WARNING, INFO, etc.
            'level': 'ERROR',
            'class': (
                'raven.contrib.django.raven_compat.handlers.SentryHandler'
            ),
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DJANGO['log_file'],
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'account': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'administrator': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'apiv1': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'billing': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'customer': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'point': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'purchase': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'shopkeeper': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'sms': {
            'handlers': ['file', 'mail_admins', 'sentry', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATIC_URL = DJANGO['static_url']

STATIC_ROOT = DJANGO['static_root']

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

MEDIA_URL = DJANGO['media_url']
MEDIA_ROOT = DJANGO['media_root']

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    # 'JS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'YUGLIFY_BINARY': '/usr/lib/node_modules/yuglify/bin/yuglify',
    'STYLESHEETS': {
        'maincss': {
            'source_filenames': (
                'css/base.css',
            ),
            'output_filename': 'css/main.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        }
    },
    'JAVASCRIPT': {
        'mainjs': {
            'source_filenames': (
                'js/main.js',
            ),
            'output_filename': 'js/main.js',
        }
    }
}

# Africa's Talking credentials
AFRICAS_TALKING_API_KEY = AFT_API['key']
AFRICAS_TALKING_USERNAME = AFT_API['user']
SENDER_ID = AFT_API['senderid']
KEY_EXPIRY_DAYS = 3
