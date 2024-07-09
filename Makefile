up_dev:
	docker compose -f docker-compose.dev.yml up --build

down_dev:
	docker compose -f docker-compose.dev.yml down

update_schedule:
	docker exec -it database_updater python3 cli.py update_schedule
