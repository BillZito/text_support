# 03 - Setup

We're almost there - there are just a couple of more steps needed
for you to be ready to develop on **text_support**.

## Get the Source

Run `git clone git@github.com:YOURFORK/text_support.git` or `git clone
git@github.com:hackmh/text_support.git` if you are a member of the hackMH
organization. We assume all other commands are being run from this directory.

## Create the development environment

As we discussed earlier, we use Docker to containerize our development environment.
Run `make build_docker` to build the development environment. Additionally, run
`make dbcreate_all` and `make dbmigrate_all`.

## Check everything worked

Run `make check`. If all tests pass, then hooray, its working! Check out
[CONTRIBUTING.md](../CONTRIBUTING.md) for more information on how to make and
submit your changes to `text_support` or continue onto
[04_developing.md](./04_developing.md) for more information on how to develop on
**text_support**.
