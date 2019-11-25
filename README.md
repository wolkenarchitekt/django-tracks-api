Django Tracks 
=============

Django Tracks is a Django web application / API to manage and play your music tracks
collection.

It is in early development stage, so features might be incomplete and stuff might break. 

Features (mostly almost done):
* Django Admin based UI for your music collection
* View/update ID3 tags using [mutagen](https://mutagen.readthedocs.io/en/latest/api/id3.html)
* Calculate audio fingerprints using [Chromaprint](https://acoustid.org/chromaprint) and save to ID3 tags
* Uses SQLite as database

Features (in progress / planned):
* Import Native Instruments collection NML
* Find duplicate audio tracks using Chromaprint

Run Django Tracks
-----------------

Django Tracks contains a Dockerfile to get started with development in no time. 
To run the development server, call:
```
make build run
```

Run tests
---------

To run all tests using pytest, call:
```
make test
```
