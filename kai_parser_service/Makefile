make_migrations:
	docker exec kai_parser_fastapi alembic revision --autogenerate -m "$(message)"

migrate:
	docker exec kai_parser_fastapi alembic upgrade heads
