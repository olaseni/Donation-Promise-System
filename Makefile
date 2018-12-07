
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