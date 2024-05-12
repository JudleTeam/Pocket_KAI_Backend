KAI_PARSER_DC=kai_parser_service/docker-compose.dev.yml
POCKET_KAI_API_DC=pocket_kai_api_service/docker-compose.dev.yml

up_all:
	docker compose -f $(POCKET_KAI_API_DC) -f $(KAI_PARSER_DC) up --build -d

down_all:
	docker compose -f $(KAI_PARSER_DC) -f $(POCKET_KAI_API_DC) down

