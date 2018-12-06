
manage-help:
	@docker-compose exec app python3 manage.py help

manage-migrate:
	@docker-compose exec app python3 manage.py migrate

manage-superuser:
	@docker-compose exec app python3 manage.py createsuperuser