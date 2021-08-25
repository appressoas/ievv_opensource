# Developing using docker

## Get docker running
(docker-compose down is not needed the first time, but it never hurts to be
absolutely sure you have no dangling processes running in the background)
```
$ cd docker/develop
$ docker-compose down
$ docker-compose build
$ docker-compose up
```

## Using the docker setup
We do not do anything other than start three docker containers:

- ``django``: The django image with all the python and javascript/css building stuff.
- ``db``: The postgres database server image.
- ``redis``: The redis server image.

We do not install python dependencies or run the django server automatically - you do that like you would locally (just via ``docker-compose exec``):

```
Install requirements:
$ docker-compose exec django pipenv install --dev

Have to run the django server on 0.0.0.0 to make it available outside the docker image:
$ docker-compose exec django pipenv run python manage.py runserver 0.0.0.0:8000

Build static files (js, css, ...)
$ docker-compose exec django pipenv run ievv buildstatic

Run the tests
$ docker-compose exec django pipenv run pytest

# Work in the shell within the container
$ docker-compose exec django bash
```

You can not use ``ievv devrun`` or ``ievv recreate_devdb`` or other dbdev related stuff
in the container - the reason for this is that we run postgres as a separate docker
container, not as something the django container has control over.
