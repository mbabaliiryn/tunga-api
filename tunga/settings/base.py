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
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

ALLOWED_HOSTS = ['tunga.io', 'web.tunga.io', 'www.tunga.io']

DEBUG = False

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

    # Social Auth Providers
    'allauth.socialaccount.providers.bitbucket_oauth2',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.twitter',

    # Local
    'tunga_auth',
    'tunga_profiles',
    'tunga_tasks',
    'tunga_messages',
    'tunga_comments',
    'tunga_utils',
    'tunga_settings',
    'tunga_activity'
]

MIDDLEWARE_CLASSES = [
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
    #'tunga_auth.middleware.UserLastActivityMiddleware',
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
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

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

DEFAULT_FROM_EMAIL = 'support@tunga.io'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'

EMAIL_USE_TLS = False

PASSWORD_HASHERS = [
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

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'VERIFIED_EMAIL': True,
    },
    'github' : {
        'SCOPE': ['user:email']
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_ADAPTER = "tunga_auth.adapter.SocialAccountAdapter"

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
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGE_SIZE': 15,
    'URL_FIELD_NAME': 'api_url',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend', 'rest_framework.filters.SearchFilter'
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'tunga_auth.serializers.TungaTokenSerializer',
    'USER_DETAILS_SERIALIZER': 'tunga_auth.serializers.UserSerializer',
    'PASSWORD_RESET_SERIALIZER': 'tunga_auth.serializers.TungaPasswordResetSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'tunga_auth.serializers.TungaRegisterSerializer',
}

SWAGGER_SETTINGS = {
    'is_authenticated': True,
    #'is_superuser': True,
    'permission_denied_handler': 'tunga_utils.views.swagger_permission_denied_handler',
}


# Local
CONTACT_REQUEST_EMAIL_RECIPIENT = 'bart@tunga.io'

TUNGA_STAFF_UPDATE_EMAIL_RECIPIENTS = ['bart@tunga.io']

TUNGA_SHARE_EMAIL = 'admin@tunga.io'

TUNGA_SHARE_PERCENTAGE = 13

TUNGA_URL = 'https://tunga.io'

GITHUB_SCOPES = ['user:email', 'repo', 'admin:repo_hook', 'admin:org_hook']
