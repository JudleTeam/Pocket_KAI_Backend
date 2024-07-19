up:
	docker compose -f docker/docker-compose.dev.yml up --build

down:
	docker compose -f docker/docker-compose.dev.yml down

make_migrations:
	docker exec pocket_kai_fastapi alembic revision --autogenerate -m "$(message)"

migrate:
	docker exec pocket_kai_fastapi alembic upgrade heads

parse_schedule:
	docker exec pocket_kai_fastapi poetry run python -m schedule_updater
