CONTAINER  = django-tracks
VIRTUALENV_DIR = .venv
HOST_UID = $(shell id -u)
HOST_GID = $(shell id -g)

DOCKER_TEST_CMD = docker run --user $(UID):$(GID) -v $(PWD):/app -p 8000:8000 -it --rm -e DJANGO_SETTINGS_MODULE=tracks_api.tests.settings $(CONTAINER)
DOCKER_CMD = docker run --user $(UID):$(GID) -v $(PWD):/app -p 8000:8000 -it --rm -e DJANGO_SETTINGS_MODULE=example_project.settings $(CONTAINER)

build:
	docker build -t $(CONTAINER) .

clean:
	-docker stop $(CONTAINER)
	-docker rm $(CONTAINER)

shell:
	docker run -v $(PWD):/app -it --rm $(CONTAINER) bash

test:
	$(DOCKER_TEST_CMD) pytest

lint:
	docker run -it --rm $(CONTAINER) flake8

mypy:
	docker run -it --rm $(CONTAINER) pytest --mypy

runserver:
	$(DOCKER_CMD) python manage.py runserver 0.0.0.0:8000

virtualenv-create:
	virtualenv --python=python3.7 $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip install -r requirements.txt
	$(VIRTUALENV_DIR)/bin/pip install -r requirements-dev.txt
	$(VIRTUALENV_DIR)/bin/pip install -e .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"

clean:
	rm -rf default.sqlite .venv build dist django_tracks.egg-info
