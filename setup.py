# !/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='django-tracks',
    packages=find_packages(exclude=['tests*']),
    author='Ingo Fischer',
    author_email='mail@ingofischer.de',
    version='0.1.0',
    install_requires=[
        'Django',
        'django-extensions',
        'django-filter',
        'django-inline-actions',
        'djangorestframework',
        'google-api-python-client',
        'gunicorn',
        'm3u8',
        'Markdown',
        'mutagen',
        'oauth2client',
        'Pillow',
        'python-magic',
        'python-mpd2',
        'PyYAML',
        'requests',
        'xmltodict',
    ],
    python_requires='>=3.6.5'
)
