.DEFAULT_GOAL := help
CONTAINER  = django-tracks
export HOST_UID=$(shell id -u)
export HOST_GID=$(shell id -g)

# Set default music dir
ifndef MUSIC_DIR
MUSIC_DIR=$(PWD)/music
endif

DOCKER_CMD = docker run --rm -it \
	-v $$(pwd):/code \
	-v django-tracks-db:/db \
	-v django-tracks-static:/static \
	-v django-tracks-media:/media \
	-v $(MUSIC_DIR):/music \
	-v /code/tests/fixtures \
	-p 8000:8000 \
	$(CONTAINER)

help:
	# Print help by extracting ##-comments per target
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:  ## Build Docker container
	docker build -t $(CONTAINER) .

django-init:
	$(DOCKER_CMD) python manage.py collectstatic --noinput
	$(DOCKER_CMD) python manage.py makemigrations
	$(DOCKER_CMD) python manage.py migrate
	$(DOCKER_CMD) python manage.py migrate --database tracks
	$(DOCKER_CMD) python manage.py create_adminuser

clean:  ## Clean database and staticfiles
	docker volume rm django-tracks-db
	docker volume rm django-tracks-static

run:  ## Run Docker container
	$(DOCKER_CMD)

shell:  ## Run Docker shell
	$(DOCKER_CMD) bash

test:  ## Run tests using pytest
	$(DOCKER_CMD) pytest tests/

update-db:  ## Update DB with ID3 data
	$(DOCKER_CMD) python manage.py update_db
