include Makefile.h

ifeq ($(MUSIC_DIR),"")
	MUSIC_DIR = $(PWD)/music
endif

DOCKER_VOLUMES = -v $(PWD):/app \
	-v $(MUSIC_DIR):/media/music \
	-v tracks_api_images:/media/images \
	-v tracks_api_db:/db \
	-v tracks_api_static:/static \
	-v tracks_api_fixtures:/media/fixtures
DOCKER_PORTS = -p $(DJANGO_TRACKS_API_PORT):8000
DOCKERFILE = Dockerfile
ifeq ($(DEV),1)
	DOCKERFILE := Dockerfile.dev
	DOCKER_NAME := $(DOCKER_NAME)_dev
endif
DOCKER_RUN_WO_PORTS = docker run $(ENV_FILES) --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_NAME)
DOCKER_RUN_W_PORTS  = docker run $(ENV_FILES) --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_PORTS) $(DOCKER_NAME)

DOCKER_TAG = riviamp/tracks-api:latest
DOCKER_AMD_TAG = riviamp/tracks-api:latest-amd64
DOCKER_ARM_TAG = riviamp/tracks-api:latest-arm32v7

PYTHON_VERSION = 3.9
VIRTUALENV_DIR = .venv

config:
	@env | grep MUSIC_DIR
	@env | grep DOCKER_*
	@env | grep TRACKS_DB_FILE

clean:
	find . \! -user $(USER) -exec sudo chown $(USER) {} \;
	-docker stop $(DOCKER_NAME)
	-docker rm $(DOCKER_NAME)
	rm -rf $(TRACKS_DB) $(VIRTUALENV_DIR) build dist django_tracks.egg-info .mypy_cache .pytest_cache
	rm -f tracks_api/migrations/0*.py

clean-db:
	rm -f db/*.sqlite
	rm -f tracks_api/migrations/0*.py
	$(MAKE) virtualenv-migrate
	$(MAKE) virtualenv-createadminuser

upgrade-requirements:
	. $(VIRTUALENV_DIR)/bin/activate && \
		pur -r requirements.txt && \
		pur -r requirements-dev.txt && \
		pur -r requirements-test.txt

pypi-convert-readme:
	pandoc --from=markdown --to=rst --output=README.rst README.md

act:
	docker build -f Dockerfile.act -t ubuntu-builder .
	act -P ubuntu-latest=ubuntu-builder

docker-build:
	docker build -t $(DOCKER_NAME) -f $(DOCKERFILE) .

docker-shell:
	$(DOCKER_RUN_WO_PORTS) bash

docker-test:
	$(MAKE) docker-build
	$(DOCKER_RUN_WO_PORTS) pytest

docker-lint:
	$(MAKE) docker-build
	$(DOCKER_RUN_WO_PORTS) pytest --lint-only --flake8 --black --mypy

docker-import:
	$(DOCKER_RUN_WO_PORTS) python manage.py import /media/music

docker-migrate:
	$(DOCKER_RUN_WO_PORTS) bash -c "python manage.py makemigrations \
		&& python manage.py migrate \
		&& python manage.py create_adminuser"

docker-collectstatic:
	$(DOCKER_RUN_W_PORTS) python manage.py collectstatic --noinput

docker-runserver:
	$(DOCKER_RUN_W_PORTS) python manage.py runserver 0.0.0.0:8000

docker-django-shell:
	$(DOCKER_RUN_WO_PORTS) python manage.py shell_plus

docker-django-urls:
	$(DOCKER_RUN_WO_PORTS) python manage.py show_urls

docker-sqlite:
	$(DOCKER_RUN_WO_PORTS) sqlite3 $(TRACKS_DB)

docker-buildx-setup:
	-docker buildx rm mybuilder
	-docker buildx create --name mybuilder
	docker buildx use mybuilder
	docker buildx inspect --bootstrap

	# Linux only - run qemu container to support armv7 on Linux:
	docker run --rm --privileged docker/binfmt:820fdd95a9972a5308930a2bdfb8573dd4447ad3

	# Linux - Arm:
	mkdir -p $(HOME)/.docker/cli-plugins/docker-buildx/
	wget https://github.com/docker/buildx/releases/download/v0.2.0/buildx-v0.2.0.linux-arm-v7 \
		-O $(HOME)/.docker/cli-plugins/docker-buildx/buildx-v0.2.0.linux-arm-v7

docker-buildx:
	docker build -t $(DOCKER_AMD_TAG) -f $(DOCKERFILE) .
	docker buildx build \
		--push \
		--platform linux/arm/v7 \
		-t $(DOCKER_ARM_TAG) \
		-f Dockerfile.arm32v7 .

docker-push:
	docker push $(DOCKER_AMD_TAG)

	-docker manifest create \
		$(DOCKER_TAG) \
		$(DOCKER_AMD_TAG) \
		$(DOCKER_ARM_TAG)
	docker manifest push $(DOCKER_TAG)

	docker manifest inspect $(DOCKER_TAG)


virtualenv-create:
	python$(PYTHON_VERSION) -m venv $(VIRTUALENV_DIR)
	. $(VIRTUALENV_DIR)/bin/activate && \
		pip install --upgrade pip setuptools && \
		pip install -r requirements.txt && \
        pip install -r requirements-dev.txt && \
        pip install -r requirements-test.txt && \
        pip install .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"

virtualenv-import:
	# Create symbolic link of your music to media/music, or set different MEDIA_ROOT
	. $(VIRTUALENV_DIR)/bin/activate && python manage.py import $$MUSIC_DIR

virtualenv-collectstatic:
	STATIC_ROOT=static/ . $(VIRTUALENV_DIR)/bin/activate && python manage.py collectstatic --noinput

virtualenv-runserver:
	TRACKS_DB_FILE=db/tracks.sqlite . $(VIRTUALENV_DIR)/bin/activate && python manage.py runserver

virtualenv-migrate:
	mkdir -p db
	TRACKS_DB_FILE=db/tracks.sqlite . $(VIRTUALENV_DIR)/bin/activate && python manage.py makemigrations
	TRACKS_DB_FILE=db/tracks.sqlite . $(VIRTUALENV_DIR)/bin/activate && python manage.py migrate
	TRACKS_DB_FILE=db/tracks.sqlite . $(VIRTUALENV_DIR)/bin/activate && python manage.py migrate --database tracks

virtualenv-format:
	. $(VIRTUALENV_DIR)/bin/activate && black tracks_api

virtualenv-createadminuser:
	. $(VIRTUALENV_DIR)/bin/activate && python manage.py create_adminuser

virtualenv-test:
	. $(VIRTUALENV_DIR)/bin/activate && pytest
