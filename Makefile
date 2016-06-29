# Makefile for common `text_support` development tasks.

DOCKER_COMPOSE=docker-compose
DOCKER_RUN=$(DOCKER_COMPOSE) run
DOCKER_IMAGE=text_support_web
WEB=web
DATABASE=db
BASH=/bin/bash -c

# `$ make build_docker`
#
# Rebuild the docker container. Do this after updating `requirements.txt`.
build_docker:
	$(DOCKER_COMPOSE) build $(WEB)

# Boot the database - many commands require this command to run first.
db_up:
	$(DOCKER_COMPOSE) up -d $(DATABASE)

# Run the tests without the extra docker commands.
local_test:
	nose2

# `$ make test`
#
# Run the tests for the application.
test: db_up
	$(DOCKER_RUN) $(WEB) $(BASH) "make local_test"

# Lint the code.
local_lint:
	pylint ./text_support

# `$ make lint`
#
# Ensure code passes all linting checks.
lint:
	$(DOCKER_RUN) $(WEB) $(BASH) "make local_lint"

# `$ make check`
#
# Ensure code is working as expected.
check: test lint

# `$ make shell`
#
# Start a shell in the development environment.
shell: db_up
	$(DOCKER_RUN) $(WEB) /bin/bash

# `$ make serve`
#
# Serve the application - accessible at http://$(DOCKER_IP):5000
serve:
	$(DOCKER_COMPOSE) up $(WEB)

# @TODO The following Makefile commands will be written as we fill in more of
# the applications behavior.

# migrate:

# deploy_create:

# deploy_update:

# Run check by default.
.DEFAULT_GOAL := check
