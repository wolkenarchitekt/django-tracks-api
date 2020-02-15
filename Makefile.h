# Convert .env-file to makefile format and export all variables
# to be accessible within make and shell commands
# Variable precedence order:
#   1) Environment variables
#   2) .env.local
#   3) .env
ifneq ("$(wildcard .env.local)","")
	output := $(shell sed "s/=/ ?= /" .env.local > /tmp/.make_env)
endif
$(shell sed "s/=/ ?= /" .env >> /tmp/.make_env)

# Export variables from merged .env files
include /tmp/.make_env
export

HOST_UID = $(shell id -u)
HOST_GID = $(shell id -g)

# Pass .env.local to Docker (overwriting variables from .env) if exists
ENV_FILES=--env-file=.env
ifneq ("$(wildcard .env.local)","")
	ENV_FILES=--env-file=.env --env-file=.env.local
endif

DOCKER_VOLUMES = -v $(PWD):/app \
	-v $(MUSIC_DIR):/media/music \
	-v tracks_api_images:/media/images \
	-v tracks_api_db:/db \
	-v tracks_api_static:/static \
	-v tracks_api_fixtures:/media/fixtures
DOCKER_PORTS = -p $(DJANGO_TRACKS_API_PORT):8000
DOCKER_WO_PORTS = docker run $(ENV_FILES) --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_NAME)
DOCKER_W_PORTS  = docker run $(ENV_FILES) --user $(UID):$(GID) $(DOCKER_VOLUMES) -it --rm $(DOCKER_PORTS) $(DOCKER_NAME)
