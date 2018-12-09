
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

manage-shell:
	@docker-compose exec app bash

manage-test:
	@docker-compose exec app python3 manage.py test

manage-tests: manage-test

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

build:
	@docker-compose build

lint:
	@flake8 django-context/src

lint-and-test: lint manage-test