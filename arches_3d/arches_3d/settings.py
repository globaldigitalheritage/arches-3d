"""
Django settings for arches_3d project.
"""

import inspect
import os
import ast
import datetime

from django.core.exceptions import ImproperlyConfigured
from arches import __version__

try:
    from arches.settings import *
except ImportError:
    pass


def get_env_variable(var_name):
    msg = "Set the %s environment variable"
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)


def get_optional_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        return None


IMAGE_VERSION = get_optional_env_variable('IMAGE_VERSION') or __version__

MODE = get_env_variable('DJANGO_MODE')  # options are either "PROD" or "DEV"
DEBUG = ast.literal_eval(get_env_variable('DJANGO_DEBUG'))
if get_optional_env_variable('DJANGO_REMOTE_DEBUG'):
    REMOTE_DEBUG = ast.literal_eval(get_optional_env_variable('DJANGO_REMOTE_DEBUG'))
else:
    REMOTE_DEBUG = False

APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
STATICFILES_DIRS = (os.path.join(APP_ROOT, 'media'),) + STATICFILES_DIRS

RESOURCE_GRAPH_LOCATIONS = (
    os.path.join(APP_ROOT, 'db', 'graphs', 'branches'), os.path.join(APP_ROOT, 'db', 'graphs', 'resource_models'))

DATATYPE_LOCATIONS.append('arches_3d.datatypes')
FUNCTION_LOCATIONS.append('arches_3d.functions')
TEMPLATES[0]['DIRS'].append(os.path.join(APP_ROOT, 'functions', 'templates'))
TEMPLATES[0]['DIRS'].append(os.path.join(APP_ROOT, 'widgets', 'templates'))
TEMPLATES[0]['DIRS'].insert(0, os.path.join(APP_ROOT, 'templates'))

TEMPLATES[0]['OPTIONS']['context_processors'].append('arches_3d.utils.context_processors.app_settings')

INSTALLED_APPS = INSTALLED_APPS + ('arches_3d', 'debug_toolbar', 'compressor')

MIDDLEWARE.remove('django.middleware.clickjacking.XFrameOptionsMiddleware')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = INTERNAL_IPS + ('172.22.0.1',)

# SECURITY WARNING: keep the secret key used in production secret!
USER_SECRET_KEY = get_optional_env_variable('DJANGO_SECRET_KEY')
# Make this unique, and don't share it with anybody.
SECRET_KEY = USER_SECRET_KEY or '1-)jb^2^7b=)ck4#)z(sypp3upwjqc8+#&ay0cj5)&wft_r!xa'


ROOT_URLCONF = 'arches_3d.urls'


ELASTICSEARCH_HTTP_PORT = get_env_variable('ESPORT')
ELASTICSEARCH_HOSTS = [
    { 'host': get_env_variable('ESHOST'), 'port': ELASTICSEARCH_HTTP_PORT }
]

# a prefix to append to all elasticsearch indexes, note: must be lower case
USER_ELASTICSEARCH_PREFIX = get_optional_env_variable('ELASTICSEARCH_PREFIX')
if USER_ELASTICSEARCH_PREFIX:
    ELASTICSEARCH_PREFIX = USER_ELASTICSEARCH_PREFIX


DATABASES = {
    'default': {
        "ATOMIC_REQUESTS": False,
        "AUTOCOMMIT": True,
        "CONN_MAX_AGE": 0,
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        "OPTIONS": {},
        'NAME': get_env_variable('PGDBNAME'),
        'USER': get_env_variable('PGUSERNAME'),
        'PASSWORD': get_env_variable('PGPASSWORD'),
        'HOST': get_env_variable('PGHOST'),
        'PORT': get_env_variable('PGPORT'),
        'POSTGIS_TEMPLATE': 'template_postgis_20',
        "TEST": {
            "CHARSET": None,
            "COLLATION": None,
            "MIRROR": None,
            "NAME": None
        },
        "TIME_ZONE": None,
    }
}

COUCHDB_URL = 'http://{}:{}@{}:{}'.format(get_env_variable('COUCHDB_USER'), get_env_variable('COUCHDB_PASS'),get_env_variable('COUCHDB_HOST'), get_env_variable('COUCHDB_PORT')) # defaults to localhost:5984

ALLOWED_HOSTS = get_env_variable('DOMAIN_NAMES').split()

SYSTEM_SETTINGS_LOCAL_PATH = os.path.join(APP_ROOT, 'system_settings', 'System_Settings.json')
WSGI_APPLICATION = 'arches_3d.wsgi.application'


STATIC_ROOT = '/static_root'
STATIC_URL = get_optional_env_variable('STATIC_URL') or '/media/'
STATIC_URL_LOCAL = get_optional_env_variable('STATIC_URL_LOCAL') or '/media/'

DEFAULT_FILE_STORAGE = 'arches_3d.storage.arches_3d_custom_storage.Arches3dCustomStorage'
STATICFILES_STORAGE = 'arches_3d.storage.arches_3d_custom_storage.Arches3dCustomStorageStatic'

STATICFILES_FINDERS = STATICFILES_FINDERS + ('compressor.finders.CompressorFinder',)

COMPRESS_ENABLED = COMPRESS_OFFLINE = not DEBUG
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE

AZURE_ACCOUNT_NAME = get_env_variable('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = get_env_variable('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = get_optional_env_variable('AZURE_CONTAINER') or 'arches'
AZURE_SSL = get_optional_env_variable('AZURE_SSL') or False
AZURE_UPLOAD_MAX_CONN = get_optional_env_variable('AZURE_UPLOAD_MAX_CONN') or 2
AZURE_CONNECTION_TIMEOUT_SECS = get_optional_env_variable('AZURE_CONNECTION_TIMEOUT_SECS') or 99999
AZURE_BLOB_MAX_MEMORY_SIZE = get_optional_env_variable('AZURE_BLOB_MAX_MEMORY_SIZE') or 2*1024*1024
AZURE_URL_EXPIRATION_SECS = get_optional_env_variable('AZURE_URL_EXPIRATION_SECS') or None
AZURE_OVERWRITE_FILES = get_optional_env_variable('AZURE_OVERWRITE_FILES') or False


RESOURCE_IMPORT_LOG = os.path.join(APP_ROOT, 'logs', 'resource_import.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(name)-12s] [%(levelname)-8s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(APP_ROOT, 'arches.log'),
            'formatter': 'default'
        }
    },
    'loggers': {
        'arches': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'arches_3d': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        '': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}


# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(APP_ROOT)

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
# It must end in a slash if set to a non-empty value.
MEDIA_URL = get_optional_env_variable('MEDIA_URL') or '/files/'

TILE_CACHE_CONFIG = {
    "name": "Disk",
    "path": os.path.join(APP_ROOT, 'tileserver', 'cache')

    # to reconfigure to use S3 (recommended for production), use the following
    # template:

    # "name": "S3",
    # "bucket": "<bucket name>",
    # "access": "<access key>",
    # "secret": "<secret key>"
}

CACHES = {
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': os.path.join(APP_ROOT, 'tmp', 'djangocache'),
    #     'OPTIONS': {
    #         'MAX_ENTRIES': 1000
    #     }
    # }
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Identify the usernames and duration (seconds) for which you want to cache the time wheel
CACHE_BY_USER = {'anonymous': 3600 * 24}

# If True, users can make edits to graphs that are locked
# (generally because they have resource intances saved against them)
# Changing this setting to True and making graph modifications may result in
# disagreement between your Resource Models and Resource Instances potentially
# causing your application to break.
# if get_optional_env_variable('OVERRIDE_RESOURCE_MODEL_LOCK'):
OVERRIDE_RESOURCE_MODEL_LOCK = True

APP_TITLE = 'Global Digital Heritage'
COPYRIGHT_TEXT = 'All Rights Reserved.'
COPYRIGHT_YEAR = datetime.datetime.now().year

try:
    from package_settings import *
except ImportError:
    pass

try:
    from settings_local import *
except ImportError:
    pass
