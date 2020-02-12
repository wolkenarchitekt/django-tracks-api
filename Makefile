include Makefile.h

DOCKER_VOLUMES = -v $(PWD):/app -v $(MUSIC_DIR):/media/music -v images:/media/images -v /app/static -v /app/tests/fixtures/music
DOCKER_ENV = -e DJANGO_SETTINGS_MODULE=tracks_site.settings
DOCKER_PORTS = -p $(DJANGO_TRACKS_API_PORT):8000
DOCKER_WO_PORTS = docker run --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_ENV) $(DOCKER_NAME)
DOCKER_W_PORTS  = docker run --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_ENV) $(DOCKER_PORTS) $(DOCKER_NAME)

TRACKS_DB = db/tracks.sqlite

build:
	docker build -t $(DOCKER_NAME) .

config:
	@env | grep MUSIC_DIR
	@env | grep DOCKER_*

clean:
	find . \! -user $(USER) -exec sudo chown $(USER) {} \;
	-docker stop $(DOCKER_NAME)
	-docker rm $(DOCKER_NAME)
	rm -rf $(TRACKS_DB) .venv build dist django_tracks.egg-info .mypy_cache .pytest_cache
	rm -f tracks_api/migrations/0*.py

format:
	black tracks_api

shell:
	$(DOCKER_WO_PORTS) bash

test:
	$(DOCKER_WO_PORTS) pytest

lint:
	$(DOCKER_WO_PORTS) pytest --lint-only --flake8 --black --mypy

virtualenv-create:
	python3.7 -m venv $(VIRTUALENV_DIR)
	. $(VIRTUALENV_DIR)/bin/activate && \
		pip install -r requirements.txt && \
        pip install -r requirements-dev.txt && \
        pip install -r requirements-test.txt && \
        pip install .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"

import:
	$(DOCKER_WO_PORTS) python manage.py import /media/music

migrate:
	$(DOCKER_WO_PORTS) python manage.py makemigrations
	$(DOCKER_WO_PORTS) python manage.py migrate
	$(DOCKER_WO_PORTS) python manage.py create_adminuser

runserver:
	$(DOCKER_W_PORTS) python manage.py runserver 0.0.0.0:8000

django-shell:
	$(DOCKER_WO_PORTS) python manage.py shell_plus

django-urls:
	$(DOCKER_WO_PORTS) python manage.py show_urls

sqlite:
	$(DOCKER_WO_PORTS) sqlite3 $(TRACKS_DB)
