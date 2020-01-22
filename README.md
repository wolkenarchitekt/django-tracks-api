# django-tracks

[![Build Status](https://travis-ci.com/ifischer/django-tracks-api.svg?branch=develop)](https://travis-ci.com/ifischer/django-tracks-api)

A Django based REST API for your music tracks

Features
--------

* import audio files (supports at least MP3, AAC, FLAC, OGG, ASF, AIFF) into Django DB.
* Can read all audio tags that [Mediafile](https://github.com/beetbox/mediafile) supports 
* Admin UI to list, show and filter tracks by tags
* *In progress: Django REST framework powered API*

Quickstart
----------

Install Django tracks API::

```shell script
pip install django-tracks-api
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'tracks_api',
    ...
)
```

Add Django tracks API's URL patterns:

```python
import tracks_api


urlpatterns = [
    ...
    url(r'^', include(tracks_api.urls)),
    ...
]
```
Run `python manage.py migrate` to create tracks API models.

Run Django server:

```shell script
python manage.py runserver
```

Screenshots
-----------

![alt text](doc/images/admin.png "Admin view")
