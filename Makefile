# Convert .env-file to makefile format and export all variables,
# so they are accessible within make and also docker compose
$(shell sed 's/=/ ?= /' .env > /tmp/.make_env)
include /tmp/.make_env
export

HOST_UID = $(shell id -u)
HOST_GID = $(shell id -g)

DOCKER_VOLUMES = -v $(PWD):/app -v $(MUSIC_DIR):/media/music -v images:/media/images -v /home/ifischer/src/mediafile:/mediafile -v /app/static
DOCKER_ENV = -e DJANGO_SETTINGS_MODULE=tracks_site.settings -e FIXTURE_DIR=/music
#DOCKER_ENV = -e DJANGO_SETTINGS_MODULE=tracks_site.settings -e FIXTURE_DIR=/music
DOCKER_PORTS = -p $(DJANGO_TRACKS_API_PORT):8000
DOCKER_TEST_CMD = docker run --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_ENV) $(DOCKER_NAME)
DOCKER_DEV_CMD  = docker run --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_ENV) $(DOCKER_PORTS) $(DOCKER_NAME)

TRACKS_DB = db/tracks.sqlite

build:
	docker build -t $(DOCKER_NAME) .

clean:
	find . \! -user $(USER) -exec sudo chown $(USER) {} \;
	-docker stop $(DOCKER_NAME)
	-docker rm $(DOCKER_NAME)
	rm -rf $(TRACKS_DB) .venv build dist django_tracks.egg-info
	-rm tracks_api/migrations/0*.py

shell:
	$(DOCKER_TEST_CMD) bash

test:
	$(DOCKER_TEST_CMD) pytest

lint:
	$(DOCKER_TEST_CMD) flake8

mypy:
	$(DOCKER_TEST_CMD) pytest --mypy

virtualenv-create:
	python3.7 -m venv $(VIRTUALENV_DIR)
	. $(VIRTUALENV_DIR)/bin/activate && \
		pip install -r requirements.txt && \
        pip install -r requirements-dev.txt && \
        pip install .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"

import:
	$(DOCKER_TEST_CMD) python manage.py import /media/music

migrate:
	$(DOCKER_TEST_CMD) python manage.py makemigrations
	$(DOCKER_TEST_CMD) python manage.py migrate

runserver:
	$(DOCKER_DEV_CMD) python manage.py runserver 0.0.0.0:8000

django-shell:
	$(DOCKER_TEST_CMD) python manage.py shell_plus
