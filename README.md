# django-tracks

[![Build Status](https://travis-ci.com/ifischer/django-tracks-api.svg?branch=develop)](https://travis-ci.com/ifischer/django-tracks-api)

A Django based REST API for your music tracks

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
