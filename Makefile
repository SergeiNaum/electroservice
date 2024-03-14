PORT ?= 8000

install:
	poetry install

dev:
	poetry run flask --app app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) app:main

lint:
	poetry run flake8 app


flask_db_init:
	flask db init  # Инициализирует каталог миграций

flask_migrate:
	flask db migrate  # Создает первичную миграцию

flask_upgrade:
	flask db upgrade  # Применяет миграцию к базе данных

flask_history:
	flask db history  # Показывает историю миграций

flask_downgrade:
	flask db downgrade <revision>  # Откатывает базу данных к указанной ревизии

make_revision:
	flask db revision --rev-id название_ревизии

make_upgrade:
	flask db upgrade название_ревизии

docker-compose_down:
	docker-compose down -v


.PHONY: install lint start

