up_dev:
	docker compose -f docker-compose.dev.yml up --build

down_dev:
	docker compose -f docker-compose.dev.yml down

update_schedule:
	docker exec -it database_updater python3 cli.py update_schedule

migrate_all:
	docker exec -it pocket_kai_fastapi alembic upgrade heads
	docker exec -it kai_parser_fastapi alembic upgrade heads
