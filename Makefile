up:
	docker compose -f docker-compose.dev.yml up --build

down:
	docker compose -f docker-compose.dev.yml down

make_migrations:
	docker exec pocket_kai_fastapi alembic revision --autogenerate -m "$(message)"

migrate:
	docker exec pocket_kai_fastapi alembic upgrade heads