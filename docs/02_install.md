# 02 - Install

Before beginning work on **text_support**, you must download the following
dependencies. For the major dependencies, we include comments on why we utilize
them - these sections can be skipped if you just want to get up and running
asap.

## Docker

We need to install [Docker](https://www.docker.com),
a platform for building and deploying
applications in containers and [docker-compose](https://docs.docker.com/compose/),
a tool for running multiple Docker containers together. A container is like a
lightweight computer which you can run on your host computer to give you access
to the development environment you need without any extra work.

#### Mac

Because Docker depends on Linux specific features, we must download additional
dependencies to set up Docker on a Mac. Luckily, everything is included in
[Docker Toolbox](https://github.com/docker/toolbox/releases/download/v1.11.2/DockerToolbox-1.11.2.pkg).
Docker Toolbox downloads every thing you need to create a virtual Linux machine on
your laptop. After installing Docker Toolbox, run through this
[setup check](http://docs.docker.com/installation/mac/#from-your-command-line)
to ensure everything is working as expected.

#### Windows

Like Mac, but a different download link for [Docker
Toolbox](https://github.com/docker/toolbox/releases/download/v1.11.2/DockerToolbox-1.11.2.exe).

#### Linux

Docker seems to have a slightly different process for installing Docker on Linux
depending on which distribution of Linux your using. Luckily, their
[installation docs](https://docs.docker.com/installation/) provide great
instructions.

### docker-compose

`docker-compose` is a tool making it possible to easily run multiple different
Docker container together.
If you downloaded `Docker` using the specified method for Mac or Windows, that
you already did everything you needed to download `docker-compose`. However, if
you downloaded `Docker` for Linux, you may also need to take additional steps to
download `docker-compose`, which can be done by following the instructions
below.

If necessary, we recommend installing `docker-compose` with the
command `sudo pip install -U docker-compose`. If you do
not have `pip`, a python dependency manager, installed follow the [install
instructions](https://pip.pypa.io/en/latest/installing.html) in their
documentation.

### Final Steps

Take a look at the remainder of this
[tutorial](https://docs.docker.com/engine/getstarted/step_one/) from Docker to
make sure everything is working as expected. If you are using `Mac` or
`Windows`, check out this [docker-machine
tutorial](https://docs.docker.com/machine/get-started/).

### Why Docker? (optional)

Docker lets us develop our applications in containers. Developing an application
on a container is like having a computer just for that application, except its a
virtual computer sitting inside your physical computer.
Using Docker is like we are all developing on the same development environment
with the same libraries, dependencies, and languages.
Any bug should be reproducible because we are all using the same development
environment. Additionally, using Docker makes deploying super easy. We just take
our application in its container, and put it on the cloud, and it runs just like
it did on our local machines. There's a bit of a learning curve to docker, but
once you get up to speed, it's very powerful. Here's an
[Intro to Docker](https://www.youtube.com/watch?v=YiZkHUbE6N0) from PyCon that
provides more context.
