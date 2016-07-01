# 04 - Developing

Now that everything is set up to being developing, there are a couple of
common tasks that you will want to know how to do. All of them include `make`
commands, making it much easier to work on this code base.

## Running Tests

Run all tests and linters with `make check`. Run `make test` to run just the
tests.

## Serving the Website

Run `make serve` to serve the website. Depending on how you are running Docker,
it will either be accessible at `http://localhost:5000` (Linux) or
`http://DOCKER-MACHINE-IP:5000` (Mac or Windows). Find `DOCKER-MACHINE-IP` with
`docker-machine ip default`.

## Accessing the Development Environment

To access a terminal within the development environment (i.e. that has all of
the python dependencies installed), run `make shell`.

## Updating the Development Environment

When we update the projects dependencies, we will need to update our Docker
development environment. Determine this by checking if either `Dockerfile` or
`requirements.txt` has changed. If so, run `make build_docker`.
