"""
Django settings for LEETCODE_REVISE project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

import os
from environ import Env
from datetime import timedelta
from urllib.parse import urlparse
import logging
env=Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',"leetcoderevisebackend-production.up.railway.app"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Third party libraries
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',        # Handles authentication
    'allauth.socialaccount',  # Enables social logins (OAuth)
    'allauth.socialaccount.providers.github',  # GitHub OAuth provider
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'LEETCODE_REVISE.urls'

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

WSGI_APPLICATION = 'LEETCODE_REVISE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

tmpPostgres = urlparse(env("DATABASE_URL"))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SITE_ID=1

SOCIALACCOUNT_PROVIDERS = {
   
    'github': {
        'APP': {
            'client_id': env("GITHUB_ID"),
            'secret': env("GITHUB_KEY"),
        },
        'AUTH_PARAMS':{
            'prompt':'consent'
        },
        'SCOPE': [
            'repo',
            'read:user',
        ],
    }
}

AUTHENTICATION_BACKENDS=(
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    
    
)

LOGIN_REDIRECT_URL='/callback/'
SOCIALACCOUNT_STORE_TOKENS=True

CORS_ORIGIN_ALLOW_ALL=True 
CORS_ALLOWS_CREDENTIALS=True

# ACCOUNT_EMAIL_REQUIRED = False  # or False if you don't want email required
SOCIALACCOUNT_AUTO_SIGNUP = True  # <== this one matters!
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
SOCIALACCOUNT_LOGIN_ON_GET = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # short-lived access token
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3650),  # 10 years = practically infinite
    "ROTATE_REFRESH_TOKENS": True,                   # rotate on each use
    "BLACKLIST_AFTER_ROTATION": True,                # blacklist old ones
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # if you're using React dev server
 "chrome-extension://bfmpdhjpaoajdjlccmdejejgdmbiolfb",  # your extension ID
   
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
     "chrome-extension://bfmpdhjpaoajdjlccmdejejgdmbiolfb",
    "https://leetcoderevisebackend-production.up.railway.app"
    
]

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

