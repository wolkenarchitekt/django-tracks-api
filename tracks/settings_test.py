from .settings import *
import os

for db in DATABASES.keys():
    DATABASES[db]['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES[db]['NAME'] = ':memory:'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'tests/fixtures/media/')

os.makedirs(os.path.join(MEDIA_ROOT, 'music'), exist_ok=True)
