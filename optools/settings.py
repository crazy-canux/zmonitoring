# -*- coding: utf-8 -*-
# Copyright (C) Canux CHENG <canuxcheng@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Django settings for optools project.

import os
import iptools

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Contacts
ADMINS = (
    ('Canux CHENG',    'canuxcheng@gmail.com'),
)

MANAGERS = ADMINS

# Default database connection if not provided by local settings. This is a testing database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',             # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'testing.db'),   # Or path to database file if using sqlite3.
        'USER': '',                                         # Not used with sqlite3.
        'PASSWORD': '',                                     # Not used with sqlite3.
        'HOST': '',                                         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
    },
}

# A list of strings representing the host/domain names that this Django site
# can serve. This is a security measure to prevent an attacker from poisoning
# caches and password reset emails with links to malicious hosts by submitting
# requests with a fake HTTP Host header, which is possible even under many
# seemingly-safe webserver configurations.
ALLOWED_HOSTS = [
    'localhost',
    'monitoring-dc.app.corp',
    'monitoring-drp.app.corp',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/static/optools/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/optools/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# LOGIN / LOGOUT
LOGIN_URL = '/optools/accounts/login/'
LOGOUT_URL = '/optools/accounts/logout/'

# SESSION MANAGEMENT
#
# Sessions are configured to be persistent with this engine.
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# Session expire when browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "monitoring.webui.context_processors.project",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'monitoring.webui.middleware.RemoteUserPersistMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'monitoring.webui.middlewares.compat.XUACompatibleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
)

ROOT_URLCONF = 'optools.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'optools.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    # Third party
    'debug_toolbar',
    'crispy_forms',
    # Monitoring WebUI
    'monitoring.webui',
    # Portal
    'apps.portal',
    # Nagios
    'apps.nagios',
    # Reporting
    'apps.kpi',
    # KB
    'apps.kb',
    # Admin interface
    'django.contrib.admin',
)

# Caching on filesystem by default
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache/optools',
    }
}

# Dokuwiki config
DOKUWIKI_BASE_URL = '/kb'
DOKUWIKI_PAGES_DIR = '/var/www/kb/data/pages'
DOKUWIKI_META_DIR = '/var/www/kb/data/meta'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Local settings
# (used for overriding values defined in this module, not part of git repo)
try:
    from optools.settings_local import *
except ImportError:
    pass

#==============================================================================
# DEBUG MODE SETTINGS
#==============================================================================
#
if DEBUG:
    # Used by some utilities (debug-toolbar, ...)
    INTERNAL_IPS = iptools.IpRangeList('127.0.0.1', '10/8', '192.168/16')

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

    # Default LOGIN / LOGOUT urls
    LOGIN_URL = '/accounts/login/'
    LOGOUT_URL = '/accounts/logout/'

    # Disable cache loader for templates in development
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    # Use Django internal db for authentication during dev
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

    # Dummy Caching in development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    # Dokuwiki config
    DOKUWIKI_BASE_URL = 'http://canuxcheng.com/kb'
    DOKUWIKI_PAGES_DIR = os.path.join(PROJECT_PATH, 'var/pages')
    DOKUWIKI_META_DIR = os.path.join(PROJECT_PATH, 'var/meta')

#==============================================================================
# LOGGING CONFIGURATION
#==============================================================================
#
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(name)-25s | %(message)s'
        },
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(name)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'monitoring.webui.log.filters.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'filters': ['require_debug_true'],
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'main_log_file':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(PROJECT_PATH, 'log/main.log'),
            'maxBytes': 10485760,
            'backupCount': 7
        },
        'jobs_log_file':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(PROJECT_PATH, 'log/jobs.log'),
            'maxBytes': 10485760,
            'backupCount': 7
        }
    },
    'loggers': {
        'apps': {
            'handlers': ['console', 'main_log_file', 'mail_admins'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'jobs': {
            'handlers': ['console', 'jobs_log_file', 'main_log_file', 'mail_admins'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
