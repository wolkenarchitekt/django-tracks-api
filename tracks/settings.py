# coding=utf-8
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'tracks.urls'
WSGI_APPLICATION = 'tracks.wsgi.application'

# logging.basicConfig(level=logging.INFO)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'inline_actions',
    # Debug
    'django_extensions',
    # third party apps
    'rest_framework',
    # local apps
    'tracks',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/db/default.sqlite'
    },
    'tracks': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/db/tracks.sqlite',
    },
}

DATABASE_ROUTERS = ['tracks.db_routers.MyDBRouter']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

SHELL_PLUS_PRE_IMPORTS = (
    ('tracks.google_image_search', '*'),
    ('tracks.models', 'fetch_track_images'),
    ('tracks.id3_utils', '*'),
    ('tracks.traktor_utils', '*'),
    ('scripts', '*'),
)

SECRET_KEY = '-02^j&_@+m#b4^yn0u_(2p2n#5d-hicd3o(3@(6au9e8@!7yox'

STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = '/static'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 50,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'  # Use JSON for all test requests
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'
MUSIC_DIR = os.environ.get('MUSIC_DIR', '/code/media/music')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'sql': {
            '()': 'tracks.utils.SQLFormatter',
            'format': '[%(duration).3f] %(statement)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'sql': {
            'class': 'logging.StreamHandler',
            'formatter': 'sql',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING'
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'INFO',
            'propagate': False
        },
        'django.db.backends.schema': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'faker': {
            'level': 'ERROR'
        },
        'PIL.PngImagePlugin': {
            'level': 'ERROR'
        },
        'parso.python.diff':  {
            'level': 'ERROR'
        },
        'urllib3.connectionpool': {
            'level': 'WARN',
        },
        'googleapiclient.discovery': {
            'level': 'WARN',
        }
    }
}
