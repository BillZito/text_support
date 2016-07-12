# Makefile for common `text_support` development tasks.

DOCKER_COMPOSE=docker-compose
DOCKER_RUN=$(DOCKER_COMPOSE) run
DOCKER_IMAGE=text_support_web
WEB=web
DATABASE=db
BASH=/bin/bash -c
HEROKU_APP=hackmh-text-support

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
	export ENVIRONMENT=TEST; nose2

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

# Copy all of the environment variables from the specified `.env*` files onto
# the Heroku platform.
set_heroku_config:
	heroku config:push --app $(HEROKU_APP) --file .env -o
	heroku config:push --app $(HEROKU_APP) --file .env.production -o

# Make sure all of the necessary add ons for the heroku platform exist.
create_add_ons:
	heroku addons:create heroku-postgresql:hobby-dev &&\
	heroku addons:create scheduler:standard
	heroku addons:create newrelic:wayne

# Helper method to delete add ons.
delete_add_ons:
	heroku addons:destroy heroku-postgresql:hobby-dev --confirm $(HEROKU_APP)
	heroku addons:destroy scheduler:standard --confirm $(HEROKU_APP)
	heroku addons:destroy newrelic:wayne --configm $(HEROKU_APP)

# Deploy code to Heroku.
#
# @TODO This method will only deploy the master branch.
deploy_code:
	git push heroku master

# `$ make deploy_create`
#
# Deploy the application for the first time to the Heroku platform.
deploy_create: set_heroku_config create_add_ons deploy_code

# `$ make deploy_update`
#
# Update the application running on the Heroku platform.
deploy_update: deploy_code

# Run check by default.
.DEFAULT_GOAL := check
