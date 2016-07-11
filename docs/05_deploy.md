# Deploy

This should only be done by the project leader.

## Deploy
- `make deploy_create` (for first time deploy).
- `make deploy_update` (for subsequent deploys).
  - These two will deploy the master branch - we actually shouldn't need to use
    either unless for some reason we need to do a manual deploy. We have set up
    continuous deployment with Travis CI (see below), which automates this
    entire process.

- We have set up continuous deployment with Travis CI such that every time the
  tests pass for us to merge to master, it will deploy. Be sure to add the
  Heroku token to travis. See info in these [Travis CI
  docs](https://docs.travis-ci.com/user/deployment/heroku/).

## Relevant Files
- [Procfile](../Procfile) specifies which processes should be run on Heroku.
- [runtime.txt](../runtime.txt) specifies which python runtime we should use on
  Heroku.

## Domain Name
- https://devcenter.heroku.com/articles/custom-domains
- https://support.cloudflare.com/hc/en-us/articles/205893698-Configure-CloudFlare-and-Heroku-over-HTTPS
