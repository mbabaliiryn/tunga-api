"""
Django settings for tunga project.
Generated by 'django-admin startproject' using Django 1.9.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!8g-9plb-5pa795jxv4@f18fu-+j^h2cyk_-?p%4s31eudmmr+'

ALLOWED_HOSTS = ["*",'tunga.io', 'web.tunga.io', 'www.tunga.io']

DEBUG = True
    
# Application definition

INSTALLED_APPS = [
    # Default
    'django.contrib.admin',
    #'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Core
    'django.contrib.sites',
    'tunga.apps.DjangoAuthConfig',
    'django.contrib.sitemaps',

    # Third Party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'tagulous',
    'actstream',
    'rest_framework',
    'oauth2_provider',
    'rest_framework_jwt',
    'rest_framework_swagger',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework.authtoken',
    'corsheaders',
    'dry_rest_permissions',
    'django_rq',
    'raven.contrib.django.raven_compat',

    # Social Auth Providers
    'allauth.socialaccount.providers.bitbucket_oauth2',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.slack',

    # Local
    'tunga_auth',
    'tunga_profiles',
    'tunga_tasks',
    'tunga_messages',
    'tunga_comments',
    'tunga_utils',
    'tunga_settings',
    'tunga_activity',
    'tunga_support',
    'tunga_pages',
]

MIDDLEWARE = [
    # Default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Local
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'tunga.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'tunga.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'tunga_auth.validators.PasswordStrengthValidator',
    }
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# Core
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'tunga/static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = (
    # Third Party
    'oauth2_provider.backends.OAuth2Backend',

    # Default
    'django.contrib.auth.backends.ModelBackend',

    # Third Party
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

AUTH_USER_MODEL = 'tunga_auth.TungaUser'

LOGIN_URL = '/'

LOGIN_REDIRECT_URL = '/'

EMAIL_SUBJECT_PREFIX = '[Tunga] '
DEFAULT_FROM_EMAIL = 'hello@tunga.io'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_USE_TLS = False

PASSWORD_HASHERS = [
    # Argon as recommended by https://docs.djangoproject.com/en/1.10/topics/auth/passwords/#using-argon2-with-django
    # Enable after upgrading to 1.10
    # 'django.contrib.auth.hashers.Argon2PasswordHasher',

    # Default
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',

    # WordPress
    'hashers_passlib.phpass',
]

# Use redis for caches
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Use the same redis as with caches for RQ
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
RQ_SHOW_ADMIN_LINK = True


# Third Party
SERIALIZATION_MODULES = {
    'xml': 'tagulous.serializers.xml_serializer',
    'json': 'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml': 'tagulous.serializers.pyyaml',
}

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX
ACCOUNT_SIGNUP_FORM_CLASS = 'tunga_auth.forms.SignupForm'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_USERNAME_BLACKLIST = ['tunga', 'tunga.io', 'admin', 'administrator', 'moderator', 'user']
ACCOUNT_ADAPTER = "tunga_auth.adapter.TungaAccountAdapter"
SOCIALACCOUNT_ADAPTER = "tunga_auth.adapter.TungaSocialAccountAdapter"

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'VERIFIED_EMAIL': True,
    },
    'github' : {
        'SCOPE': ['user:email']
    },
    'slack': {
        'SCOPE': ['identity.basic', 'identity.email', 'identity.avatar', 'identity.team']
    }
}
SOCIALACCOUNT_AUTO_SIGNUP = True

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'},
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'ACCESS_TOKEN_EXPIRE_SECONDS': 120*24*60*60  # 120 days
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': 'tunga_utils.pagination.DefaultPagination',
    'URL_FIELD_NAME': 'api_url',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter'
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'tunga_auth.serializers.TungaTokenSerializer',
    'USER_DETAILS_SERIALIZER': 'tunga_auth.serializers.UserSerializer',
    'PASSWORD_RESET_SERIALIZER': 'tunga_auth.serializers.TungaPasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'tunga_auth.serializers.TungaPasswordResetConfirmSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'tunga_auth.serializers.TungaRegisterSerializer',
}

SWAGGER_SETTINGS = {
    'is_authenticated': True,
    #'is_superuser': True,
    'permission_denied_handler': 'tunga_utils.helpers.swagger_permission_denied_handler',
}


# Local
TUNGA_NAME = 'Tunga'
TUNGA_CONTACT_REQUEST_EMAIL_RECIPIENTS = ['bart@tunga.io']
TUNGA_STAFF_LOW_LEVEL_UPDATE_EMAIL_RECIPIENTS = ['bart@tunga.io', 'david@tunga.io', 'domieck@tunga.io', 'eric@tunga.io']
TUNGA_STAFF_UPDATE_EMAIL_RECIPIENTS = TUNGA_STAFF_LOW_LEVEL_UPDATE_EMAIL_RECIPIENTS
TUNGA_SHARE_EMAIL = 'admin@tunga.io'
TUNGA_SHARE_PERCENTAGE = 13
TUNGA_URL = 'https://tunga.io'

TUNGA_FEE_DEV = 19
TUNGA_FEE_PM = 39

TUNGA_PERCENTAGE_DEV = 37.5
TUNGA_PERCENTAGE_PM = 100

TUNGA_PM_TIME_RATIO = 0.15

SOCIAL_CONNECT_ACTION = 'action'
SOCIAL_CONNECT_NEXT = 'next'
SOCIAL_CONNECT_USER_TYPE = 'user_type'
SOCIAL_CONNECT_TASK = 'task'
SOCIAL_CONNECT_CALLBACK = 'connect_callback'

SOCIAL_CONNECT_ACTION_REGISTER = 'register'
SOCIAL_CONNECT_ACTION_CONNECT = 'connect'

GITHUB_SCOPES = ['user:email', 'repo', 'admin:repo_hook', 'admin:org_hook']

STRIPE_SECRET = ''

COINBASE_API_KEY = ''
COINBASE_API_SECRET = ''
COINBASE_CLIENT_ID = ''
COINBASE_CLIENT_SECRET = ''
COINBASE_SCOPES = ['wallet:accounts:read', 'wallet:addresses:create']
COINBASE_BASE_URL = 'https://www.coinbase.com'
COINBASE_BASE_API_URL = 'https://api.coinbase.com'

BITONIC_CONSUMER_KEY = ''
BITONIC_CONSUMER_SECRET = ''
BITONIC_ACCESS_TOKEN = ''
BITONIC_TOKEN_SECRET = ''
BITONIC_URL = 'https://bitonic.nl/order'
BITONIC_PAYMENT_COST_PERCENTAGE = 3

BANK_TRANSFER_PAYMENT_COST_PERCENTAGE = 5.5

BITPESA_API_KEY = ''
BITPESA_API_SECRET = ''
BITPESA_API_URL = 'https://api.bitpesa.co/v1/'
BITPESA_SENDER = None

SLACK_STAFF_INCOMING_WEBHOOK = None
SLACK_STAFF_OUTGOING_WEBHOOK_TOKEN = None
SLACK_DEVELOPER_INCOMING_WEBHOOK = None
SLACK_DEBUGGING_INCOMING_WEBHOOK = None
SLACK_CLIENT_ID = None
SLACK_CLIENT_SECRET = None
SLACK_ACCESS_TOKEN_URL = 'https://slack.com/api/oauth.access'
SLACK_AUTHORIZE_URL = 'https://slack.com/oauth/authorize'
SLACK_SCOPES = [
    'identify',
    'channels:history', 'channels:read', 'channels:write',
    'chat:write:bot', 'im:write',
    'users:read', 'users.profile:read', 'users:read.email'
    # 'bot'
]

SLACK_STAFF_UPDATES_CHANNEL = '#updates'
SLACK_STAFF_MISSED_UPDATES_CHANNEL = '#missed-updates'
SLACK_STAFF_LEADS_CHANNEL = '#platformleads'
SLACK_STAFF_CUSTOMER_CHANNEL = '#customers'
SLACK_STAFF_PROJECT_EXECUTION_CHANNEL = '#projectexecution'
SLACK_STAFF_PAYMENTS_CHANNEL = '#payments'
SLACK_STAFF_PROFILES_CHANNEL = '#profiles'
SLACK_STAFF_HUBSPOT_CHANNEL = '#hubspot'
SLACK_DEVELOPER_UPDATES_CHANNEL = '#general'
SLACK_PMS_UPDATES_CHANNEL = '#projects'

SLACK_ATTACHMENT_COLOR_TUNGA = '#EE1F54'
SLACK_ATTACHMENT_COLOR_NEUTRAL = '#CCC'
SLACK_ATTACHMENT_COLOR_GREEN = '#4CAF50'
SLACK_ATTACHMENT_COLOR_RED = '#FF0000'
SLACK_ATTACHMENT_COLOR_BLUE = '#0078BD'

TUNGA_ICON_URL_150 = 'https://tunga.io/icons/Tunga_iconx150.png'
TUNGA_ICON_SQUARE_URL_150 = 'https://tunga.io/icons/Tunga_squarex150.png'

HARVEST_CLIENT_ID = None
HARVEST_CLIENT_SECRET = None
HARVEST_API_URL = 'https://api.harvestapp.com'
HARVEST_ACCOUNT = ''
HARVEST_AUTHENTICATION_STRING = ''

HUBSPOT_API_KEY = None
HUBSPOT_DEFAULT_DEAL_PIPELINE = 'default'
HUBSPOT_DEFAULT_DEAL_STAGE_NEW_USER = HUBSPOT_DEFAULT_DEAL_STAGE_MEMBER = 'appointmentscheduled'
HUBSPOT_DOMIECK_OWNER_ID = ''


MAILCHIMP_USERNAME = None
MAILCHIMP_API_KEY = None
MAILCHIMP_NEW_USER_LIST = None
MAILCHIMP_NEW_USER_AUTOMATION_WORKFLOW_ID = None
MAILCHIMP_NEW_USER_AUTOMATION_EMAIL_ID = None

MANDRILL_API_KEY = None
MANDRILL_VAR_SUBJECT = 'subject'
MANDRILL_VAR_FIRST_NAME = 'first_name'


PAYONEER_USERNAME = None
PAYONEER_PASSWORD = None
PAYONEER_PARTNER_ID = None
PAYONEER_API_URL = None

EXACT_DOCUMENT_TYPE_SALES_INVOICE = None
EXACT_DOCUMENT_TYPE_PURCHASE_INVOICE = None

RAVEN_CONFIG = {
    'dsn': '',  # Raven URL here
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

try:
    from .env.dev import *
except ImportError:
    from .env.production import *


if DEBUG:
    for template_engine in TEMPLATES:
        template_engine['OPTIONS']['debug'] = True
