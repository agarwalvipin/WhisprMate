.PHONY: build deploy up down ruff ruff-fix test-docker test-local

build:
	docker compose build

deploy:
	./scripts/deploy.sh

up:
	docker compose up -d

down:
	docker compose down

ruff:
	ruff check .

ruff-fix:
	ruff check . --fix

test-docker:
	./test_docker.sh

test-local:
	./test_app.sh