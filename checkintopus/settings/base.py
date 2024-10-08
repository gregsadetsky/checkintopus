import os
import uuid
from pathlib import Path

import dj_database_url
from django.utils.log import DEFAULT_LOGGING
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# DEBUG set to False by default
DEBUG = False

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
CSRF_TRUSTED_ORIGINS = os.environ["CSRF_TRUSTED_ORIGINS"].split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    # https://github.com/skorokithakis/django-loginas
    "loginas",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "checkintopus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "checkintopus.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
AUTH_USER_MODEL = "core.User"

RC_OAUTH_APP_ID = os.environ["RC_OAUTH_APP_ID"]
RC_OAUTH_APP_SECRET = os.environ["RC_OAUTH_APP_SECRET"]
RC_OAUTH_REDIRECT_URI = os.environ["RC_OAUTH_REDIRECT_URI"]

AUTHLIB_OAUTH_CLIENTS = {
    "rc": {
        "client_id": os.environ["RC_OAUTH_APP_ID"],
        "client_secret": os.environ["RC_OAUTH_APP_SECRET"],
        "api_base_url": "https://www.recurse.com/api/v1/",
        "authorize_url": "https://www.recurse.com/oauth/authorize",
        "access_token_url": "https://www.recurse.com/oauth/token",
    }
}

RASPI_SCAN_UUID_API_KEY = os.environ["RASPI_SCAN_UUID_API_KEY"]
assert RASPI_SCAN_UUID_API_KEY and len(RASPI_SCAN_UUID_API_KEY) == 36
# the following will fail if the given key is not a uuid
_ = uuid.UUID(RASPI_SCAN_UUID_API_KEY)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
# https://whitenoise.readthedocs.io/en/latest/django.html
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": os.environ["AWS_STORAGE_BUCKET_NAME"],
        },
    },
}

# start from default values -- so that they can be overriden later
# https://stackoverflow.com/a/25508761
LOGGING = DEFAULT_LOGGING

# to not be redirected to /accounts/profile after logging out of the admin
LOGIN_REDIRECT_URL = "/"
