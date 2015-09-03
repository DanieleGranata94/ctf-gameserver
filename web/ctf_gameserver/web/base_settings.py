"""
Common Django settings for the web part of 'ctf-gameserver'.
You should not have to edit this file for out-of-the-box usage, but of course it's customizable just as the
rest of the code.
"""

import os

# This file's directory, to conveniently build absolute paths using `os.path.join(BASE_DIR, )`
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'ctf_gameserver.web.registration',
    'ctf_gameserver.web.scoring'
)

# Ordering of the middlewares is important, see
# https://docs.djangoproject.com/en/1.8/ref/middleware/#middleware-ordering
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.static'
        ]
    }
}]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

ROOT_URLCONF = 'ctf_gameserver.web.urls'
WSGI_APPLICATION = 'ctf_gameserver.web.wsgi.application'

STATIC_URL = '/static/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = ''    # TODO

# We're prepared for translations, but don't provide them out-of-the-box; most internationalization features
# can therefore be disabled
USE_I18N = False
USE_TZ = True
LANGUAGE_CODE = 'en-us'
THOUSAND_SEPARATOR = ' '
NUMBER_GROUPING = 3

TIME_FORMAT = 'H:i'
MONTH_DAY_FORMAT = 'j F'
DATE_FORMAT = MONTH_DAY_FORMAT + ' Y'
SHORT_DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT
SHORT_DATETIME_FORMAT = SHORT_DATE_FORMAT + ' ' + TIME_FORMAT

CSRF_COOKIE_HTTPONLY = True
PASSWORD_RESET_TIMEOUT_DAYS = 1
