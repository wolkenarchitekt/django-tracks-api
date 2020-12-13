import os

DEBUG = "DEBUG" in os.environ
SECRET_KEY = "fake-key"
ROOT_URLCONF = "tracks_api.urls"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = "*"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "tracks_api",
]
if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ["django_extensions"]

TRACKS_DB_FILE = os.environ.get(
    "TRACKS_DB_FILE", os.path.join(BASE_DIR, "db/tracks.sqlite")
)

DEFAULT_DB_FILE = os.environ.get(
    "DEFAULT_DB_FILE", os.path.join(BASE_DIR, "db/default.sqlite")
)

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DEFAULT_DB_FILE},
    "tracks": {"ENGINE": "django.db.backends.sqlite3", "NAME": TRACKS_DB_FILE}
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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
            ]
        },
    }
]

STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_ROOT = os.environ.get("STATIC_ROOT", os.path.join(BASE_DIR, "static"))

# MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
# MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

MUSIC_URL = "/music/"
MUSIC_ROOT = os.environ["MUSIC_ROOT"]
# MEDIA_ROOT = os.environ.get("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

# MUSIC_DIR = os.environ.get("MUSIC_DIR", None)
# if MUSIC_DIR:
#     MUSIC_DIR = os.path.expanduser(MUSIC_DIR)
#     MEDIA_ROOT = MUSIC_DIR

STATICFILES_DIRS = [
    MUSIC_ROOT,
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",  # Use JSON for all test requests
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
        "django.db.backends": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "asyncio": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        }
    },
}
