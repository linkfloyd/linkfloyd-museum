# -*- coding: utf-8 -*-

import os

ugettext = lambda s: s # dummy ugettext function, as django's docs say

from local_settings import *

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Mirat Can Bayrak', 'miratcanbayrak@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'sqlite.db'),
    }
}

TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "sitestatic"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@3r4omh@3o3^pc00leu6m871x@o$e0k1^@&n-k4+zsq&3l!ixi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'linkfloyd.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    # contrib
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # linkfloyd
    'linkfloyd.links',
    'linkfloyd.preferences',
    'linkfloyd.channels',
    'linkfloyd.comments',
    'linkfloyd.summaries',

    # 3th party
    'django_extensions',
    'sorl.thumbnail',
    'qhonuskan_votes',
    'registration',
    'gravatar',
    'south',
    'devserver',
    'invitation',
)

DEVSERVER_IGNORED_PREFIXES = ['/media', '/uploads']
DEVSERVER_MODULES = (
    'devserver.modules.profile.LineProfilerModule',
    'devserver.modules.ajax.AjaxDumpModule',
)

# EMAIL
SERVER_EMAIL = 'server@linkfloyd.com'
SEND_BROKEN_LINK_EMAILS=True
DEFAULT_FROM_EMAIL = "noreply@linkfloyd.com"



# REGISTRATION
ACCOUNT_ACTIVATION_DAYS = 3
LOGIN_REDIRECT_URL = "/"

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda user: "/links/from/%s/" % user.username,
}

# GRAVATAR
GRAVATAR_DEFAULT_IMAGE = "mm"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

