.PHONY: install migrate run test clean

install:
	uv sync

migrate:
	uv run python manage.py migrate

run:
	uv run python manage.py runserver


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf staticfiles/
	rm -f debug.log

superuser:
	uv run python manage.py createsuperuser

shell:
	uv run python manage.py shell

collectstatic:
	uv run python manage.py collectstatic --noinput
