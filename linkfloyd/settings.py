# -*- coding: utf-8 -*-

import os

ugettext = lambda s: s  # dummy ugettext function, as django's docs say

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__.decode('utf-8')))

ADMINS = (('Mirat Can Bayrak', 'miratcanbayrak@gmail.com'),)
SERVER_EMAIL = "django@linkfloyd.com"
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'sqlite3.db')}}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'tr'
LANGUAGES = (('tr', 'Türkçe'), ('en', 'English'))
SITE_ID = 1
USE_I18N = True
USE_L10N = False

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

MEDIA_URL = "/media/"
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "sitestatic/"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

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
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'seo_cascade.middleware.SEOMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    )

ROOT_URLCONF = 'linkfloyd.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = [
    # contrib
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

    # linkfloyd
    'linkfloyd.links',
    'linkfloyd.preferences',
    'linkfloyd.channels',
    'linkfloyd.comments',
    'linkfloyd.summaries',
    'linkfloyd.wiki',
    'linkfloyd.notifications',

    # 3th party
    'sorl.thumbnail',
    'qhonuskan_votes',
    'registration',
    'gravatar',
    'seo_cascade',
    'pipeline',
]

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
  'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': (
            'css/style.less',
        ),
        'output_filename': 'css/b.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_LESS_BINARY = "~/node_modules/less/bin/lessc"

# EMAIL

SEND_BROKEN_LINK_EMAILS = True
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

from local_settings import *
