CONTAINER  = django-tracks
VIRTUALENV_DIR = .venv

build:
	docker build -t $(CONTAINER) .

clean:
	-docker stop $(CONTAINER)
	-docker rm $(CONTAINER)

shell:
	docker run -v $(PWD):/app -it --rm $(CONTAINER) bash

test:
	docker run -it -e DJANGO_SETTINGS_MODULE=tracks_api.tests.settings --rm $(CONTAINER) pytest

lint:
	docker run -it --rm $(CONTAINER) flake8

mypy:
	docker run -it --rm $(CONTAINER) pytest --mypy

virtualenv-create:
	virtualenv --python=python3.7 $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip install -r requirements.txt
	$(VIRTUALENV_DIR)/bin/pip install -r requirements-dev.txt
	$(VIRTUALENV_DIR)/bin/pip install -e .
	@echo "Activate virtualenv:\n. $(VIRTUALENV_DIR)/bin/activate"


