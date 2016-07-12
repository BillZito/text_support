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

# Create the development database.
dbcreate_dev: db_up
	$(DOCKER_RUN) $(WEB) python manage.py create_db

# Create the test database.
dbcreate_test: db_up
	$(DOCKER_RUN) $(WEB) bash -c "export ENVIRONMENT=TEST; python manage.py create_db"

# `$ make dbcreate_all`
#
# Create the test and development databases.
dbcreate_all: dbcreate_dev dbcreate_test

# Migrate the development database.
dbmigrate_dev: db_up
	$(DOCKER_RUN) $(WEB) python manage.py db upgrade

# Migrate the test database.
dbmigrate_test: db_up
	$(DOCKER_RUN) $(WEB) bash -c "export ENVIRONMENT=TEST; python manage.py db upgrade"

# `$ make dbmigrate_all`
#
# Migrate both the development and test databases.
dbmigrate_all: dbmigrate_dev dbmigrate_test

# `$ make generate_migration`
#
# Generate the files for a migration.
generate_migration: db_up
	$(DOCKER_RUN) $(WEB) python manage.py db migrate

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

# Create the production database.
dbcreate_prod:
	heroku run python manage.py create_db --app $(HEROKU_APP)

# Migrate the production database.
dbmigrate_prod:
	heroku run python manage.py db upgrade --app $(HEROKU_APP)

# `$ make deploy_create`
#
# Deploy the application for the first time to the Heroku platform.
deploy_create: set_heroku_config create_add_ons deploy_code dbcreate_prod dbmigrate_prod

# `$ make deploy_update`
#
# Update the application running on the Heroku platform.
deploy_update: deploy_code dbmigrate_prod

# Run check by default.
.DEFAULT_GOAL := check
