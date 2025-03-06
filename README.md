# Climbing-Comp Tracker

A basic toolset to track independent climbing statistics for individuals and teams.

Intended to have "beautiful data visualization" to help make tracking stats "cool" and useful.

## Building

Build both images and publish to docker registry

```sh
docker build -t jcookin/climbing-comp:latest -t jcookin/climbing-comp:<version>
```

## Running

Image is available on [docker hub](https://hub.docker.com/r/jcookin/climbing-comp)

## Deploying

Deploy to kubernetes with the 'deploy/k8s.yml' configuration.

Docker deployment is trivial, so long as the Grafana dashboard is not in use, in which case additional configurations are required.

Grafana dashboard is available as a subpath to the root domain in the kubernetes manifest.
It can be accessed at `/dashboard`.
