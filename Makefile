
manage-help:
	@docker-compose exec app python3 manage.py help

manage-superuser:
	@docker-compose exec app python3 manage.py createsuperuser

manage-startapp:
	@docker-compose exec app python3 manage.py startapp dps_main

manage-showmigrations:
	@docker-compose exec app python3 manage.py showmigrations

manage-makemigrations:
	@docker-compose exec app python3 manage.py makemigrations

manage-migrate:
	@docker-compose exec app python3 manage.py migrate

manage-pyshell:
	@docker-compose exec app python3 manage.py shell

manage-dbshell:
	@docker-compose exec app python3 manage.py dbshell

manage-test: export DJANGO_SETTINGS_MODULE=dps.settings.test
manage-test:
	@docker-compose run app test

manage-tests: manage-test

app-shell:
	@docker-compose exec app bash

app-python3:
	@docker-compose exec app python3

down:
	@docker-compose down

up:
	@docker-compose up -d

start: up
run: up

restart: down up
down-up: restart

logs:
	@docker-compose logs

logsf:
	@docker-compose logs -f --tail=20

app-logs:
	@docker-compose logs -f --tail=20 app

lint:
	@flake8 django-context/src

lint-and-test: lint manage-test

build: lint-and-test

docker-build-image:
	# Builds the python-django image
	@docker build -t olaseni/python-django:dps-1.0 django-context

docker-build-and-push-image: docker-build-image
	# Builds and pushes the python-django image to docker hub in one fell swoop
	# Requires docker login or the `push` leg will fail
	@docker login
	@docker push olaseni/python-django:dps-1.0