.PHONY: install dev build down reset logs shell db migrate secret help

# ── Setup ─────────────────────────────────────────────────────────────────────

install: ## First-time setup after cloning
	@cp -n .env.example .env 2>/dev/null && echo "Created .env from .env.example" || echo ".env already exists"
	uv sync
	docker compose up -d db
	@echo "Waiting for database..."
	@docker compose exec db sh -c 'until pg_isready -U tms -d tms_db; do sleep 1; done'
	uv run alembic upgrade head
	@echo ""
	@echo "✓ Setup complete. Run 'make dev' to start."

# ── Run ───────────────────────────────────────────────────────────────────────

dev: ## Start DB in Docker, app locally with hot reload (recommended)
	docker compose up -d db
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

build: ## Run full stack in Docker (uses Dockerfile)
	docker compose up --build

down: ## Stop everything
	docker compose down

reset: ## Wipe DB volume and start fresh
	docker compose down -v
	$(MAKE) install

# ── Utilities ─────────────────────────────────────────────────────────────────

logs: ## Tail app logs (Docker only)
	docker compose logs -f app

shell: ## Shell into the app container (Docker only)
	docker compose exec app sh

db: ## Open psql in the DB container
	docker compose exec db psql -U tms -d tms_db

migrate: ## Run pending migrations
	uv run alembic upgrade head

secret: ## Generate a new SECRET_KEY
	@openssl rand -hex 32

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
