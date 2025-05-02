run:
	chmod +x ./load_env.sh \
	&& . ./load_env.sh \
	&& poetry run uvicorn teawish.main:app --host 0.0.0.0 --port 8000 --reload

make_migration:
	@if [ -z "$(NAME)" ]; then \
		echo "Error: migration name undefined. Use: make make_migration NAME='your_name'"; \
		exit 1; \
	fi
	@poetry run alembic revision --autogenerate -m "$(NAME)"

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

lint:
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files
