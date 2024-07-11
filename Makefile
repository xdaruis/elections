SHELL := /bin/bash

lint:
	docker-compose run --rm app sh -c "flake8"

test:
	docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"

migrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations"

build-prod:
	docker-compose -f docker-compose-deploy.yml build

start-prod:
	docker-compose -f docker-compose-deploy.yml up

generate_env:
	@echo "DB_NAME=dbname" > .env
	@echo "DB_USER=rootuser" >> .env
	@echo "DB_PASSWORD=password" >> .env
	@echo "DJANGO_SECRET_KEY=$$(python3 -c 'import secrets; print(secrets.token_hex(100))')" >> .env
	@echo "DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0" >> .env
	@echo ".env file generated successfully!"
	@echo "" >> .env.backup
	@echo $(shell date +'%d.%m.%Y %H:%M:%S') >> .env.backup
	@cat .env >> .env.backup
