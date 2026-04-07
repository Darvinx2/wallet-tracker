COMPOSE = docker compose -f deploy/docker-compose.yml

.PHONY: up down restart build logs ps

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

build:
	$(COMPOSE) build
