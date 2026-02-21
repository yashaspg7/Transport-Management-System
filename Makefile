.PHONY: install dev build down reset db migrate migration ci secret help

# ── Setup ─────────────────────────────────────────────────────────────────────

install: ## First-time setup after cloning
	@cp -n .env.example .env 2>/dev/null && echo "Created .env from .env.example" || echo ".env already exists"
	uv sync
	docker compose up -d db
	@echo "Waiting for database..."
	@timeout 30 sh -c 'until docker compose exec db pg_isready -U tms -d tms_db 2>/dev/null; do sleep 1; done' \
		|| (echo "❌ Database failed to start within 30 seconds" && exit 1)
	uv run alembic upgrade head
	@echo ""
	@echo "✓ Setup complete. Run 'make dev' to start."

# ── Run ───────────────────────────────────────────────────────────────────────

dev: ## Start DB in Docker, app locally with hot reload
	docker compose up -d db
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

build: ## Run full stack in Docker (uses Dockerfile)
	docker compose up --build

down: ## Stop all Docker containers
	docker compose down

reset: ## Wipe DB volume and reinstall fresh
	docker compose down -v
	$(MAKE) install

# ── Database ──────────────────────────────────────────────────────────────────

db: ## Open psql in the DB container
	docker compose exec db psql -U tms -d tms_db

migrate: ## Run pending Alembic migrations
	uv run alembic upgrade head

migration: ## Create a new migration (usage: make migration "your message")
	uv run alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

# ── CI ────────────────────────────────────────────────────────────────────────

ci: ## Run full CI pipeline locally (lint, format, typecheck, tests)
	uv run scripts/run-ci.py

# ── Utilities ─────────────────────────────────────────────────────────────────

secret: ## Generate a new SECRET_KEY
	@openssl rand -hex 32

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

%:
	@:
