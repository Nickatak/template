.PHONY: help \
	local-venv local-install local-install-frontend local-install-backend \
	local-up local-run local-run-frontend local-run-backend local-kill-ports \
	local-migrate local-seed local-test local-test-api local-test-e2e local-test-cov \
	local-pre-commit-install local-clean \
	dev-build dev-up dev-down dev-logs dev-shell-backend dev-shell-mysql dev-migrate dev-seed dev-test \
	prod-build prod-up prod-down prod-logs prod-seed

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PYTEST := $(VENV_DIR)/bin/pytest
LOCAL_API_BASE_URL ?= http://localhost:8000/api
LOCAL_KILL_PORTS ?= 8000 3000
DEV_COMPOSE := docker compose
PROD_COMPOSE := docker compose -f docker-compose.yml -f docker-compose.staging.yml

# ============================================================================
# HELP
# ============================================================================

help:
	@echo "Template Repository - Development Commands"
	@echo ""
	@echo "Local Commands:"
	@echo "  make local-install        - Install frontend and backend dependencies"
	@echo "  make local-install-backend - Install backend dependencies only"
	@echo "  make local-install-frontend - Install frontend dependencies only"
	@echo "  make local-up             - Run backend + frontend local dev servers"
	@echo "  make local-kill-ports     - Stop listeners on common local ports"
	@echo "  make local-run-backend    - Start Django local dev server"
	@echo "  make local-run-frontend   - Start Next.js local dev server"
	@echo "  make local-migrate        - Apply Django migrations"
	@echo "  make local-test           - Run all tests"
	@echo "  make local-test-api       - Run API tests only"
	@echo "  make local-test-e2e       - Run E2E tests only"
	@echo "  make local-test-cov       - Run tests with coverage report"
	@echo "  make local-pre-commit-install - Install pre-commit hooks"
	@echo "  make local-seed           - Seed database with initial data"
	@echo "  make local-clean          - Remove local build artifacts and cache"
	@echo ""
	@echo "Dev Docker Commands:"
	@echo "  make dev-build            - Build Docker images"
	@echo "  make dev-up               - Start Docker stack in foreground"
	@echo "  make dev-down             - Stop and remove Docker stack"
	@echo "  make dev-logs             - Stream Docker logs"
	@echo "  make dev-shell-backend    - Open shell in backend container"
	@echo "  make dev-shell-mysql      - Open MySQL shell in mysql container"
	@echo "  make dev-migrate          - Run backend migrations in container"
	@echo "  make dev-seed             - Seed database with initial data in container"
	@echo "  make dev-test             - Run backend tests in container"
	@echo ""
	@echo "Staging Docker Commands:"
	@echo "  make prod-build           - Build Docker images with staging override"
	@echo "  make prod-up              - Start staging stack in detached mode"
	@echo "  make prod-down            - Stop staging stack"
	@echo "  make prod-logs            - Stream staging stack logs"
	@echo "  make prod-seed            - Seed database with initial data in staging"
	@echo ""
	@echo "Override frontend API URL with:"
	@echo "  make local-run-frontend LOCAL_API_BASE_URL=http://localhost:8000/api"

# ============================================================================
# LOCAL
# ============================================================================

local-venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

local-install: local-venv local-install-backend local-install-frontend
	@echo "Setting up environment files..."
	@[ -f .env.dev ] || cp .env.example .env.dev
	@[ -f .env.prod ] || cp .env.example .env.prod
	./scripts/toggle-env.sh dev
	$(PYTHON) manage.py migrate

local-install-backend: local-venv
	$(PIP) install -r requirements.txt

local-install-frontend:
	npm install --prefix frontend

local-up: local-kill-ports
	@echo "Starting frontend and backend servers (press Ctrl+C to stop both)..."
	@set -e; \
	$(MAKE) local-run-frontend & frontend_pid=$$!; \
	$(MAKE) local-run-backend & backend_pid=$$!; \
	cleanup() { \
		echo "Stopping local servers..."; \
		kill $$frontend_pid $$backend_pid 2>/dev/null || true; \
		pkill -TERM -P $$frontend_pid 2>/dev/null || true; \
		pkill -TERM -P $$backend_pid 2>/dev/null || true; \
		wait $$frontend_pid $$backend_pid 2>/dev/null || true; \
	}; \
	trap 'cleanup; exit 130' INT TERM; \
	wait $$frontend_pid $$backend_pid || true; \
	cleanup

local-run: local-run-frontend

local-kill-ports:
	@echo "Stopping listeners on ports: $(LOCAL_KILL_PORTS)"
	@for port in $(LOCAL_KILL_PORTS); do \
		if command -v fuser >/dev/null 2>&1; then \
			echo "Port $$port: sending TERM"; \
			fuser -k -TERM $$port/tcp 2>/dev/null || true; \
			sleep 1; \
			if fuser $$port/tcp >/dev/null 2>&1; then \
				echo "Port $$port: still busy, sending KILL"; \
				fuser -k -KILL $$port/tcp 2>/dev/null || true; \
			fi; \
		elif command -v lsof >/dev/null 2>&1; then \
			pids="$$(lsof -tiTCP:$$port -sTCP:LISTEN 2>/dev/null || true)"; \
			if [ -n "$$pids" ]; then \
				echo "Port $$port: sending TERM to PID(s) $$pids"; \
				kill -TERM $$pids 2>/dev/null || true; \
				sleep 1; \
				pids="$$(lsof -tiTCP:$$port -sTCP:LISTEN 2>/dev/null || true)"; \
				if [ -n "$$pids" ]; then \
					echo "Port $$port: still busy, sending KILL to PID(s) $$pids"; \
					kill -KILL $$pids 2>/dev/null || true; \
				fi; \
			else \
				echo "Port $$port: no listener"; \
			fi; \
		else \
			echo "Port $$port: skipped (install fuser or lsof)"; \
		fi; \
	done
	@echo "--- verification ---"; \
	for port in $(LOCAL_KILL_PORTS); do \
		if ss -ltn "( sport = :$$port )" | tail -n +2 | grep -q .; then \
			echo "Port $$port: still in use"; \
		else \
			echo "Port $$port: free"; \
		fi; \
	done

local-run-frontend:
	NEXT_PUBLIC_API_URL=$(LOCAL_API_BASE_URL) npm run dev --prefix frontend

local-run-backend:
	$(PYTHON) manage.py runserver

local-migrate:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

local-seed:
	$(PYTHON) manage.py seed_dev

local-test:
	$(PYTEST) tests/ -v

local-test-api:
	$(PYTEST) tests/test_auth_api.py -v

local-test-e2e:
	@echo "Ensure frontend/backend are running on ports 3000 and 8000 before E2E tests."
	$(PYTEST) tests/test_auth_e2e.py -v

local-test-cov:
	$(PYTEST) tests/ -v --cov=api --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

local-pre-commit-install:
	$(PYTHON) -m pre_commit install

local-clean:
	rm -rf frontend/.next frontend/out htmlcov .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete."

# ============================================================================
# DEV DOCKER
# ============================================================================

dev-build:
	$(DEV_COMPOSE) build

dev-up:
	$(DEV_COMPOSE) up --build

dev-down:
	$(DEV_COMPOSE) down

dev-logs:
	$(DEV_COMPOSE) logs -f

dev-shell-backend:
	$(DEV_COMPOSE) exec backend sh

dev-shell-mysql:
	$(DEV_COMPOSE) exec mysql mysql -u$${MYSQL_USER:-template} -p$${MYSQL_PASSWORD:-template} $${MYSQL_DATABASE:-template}

dev-migrate:
	$(DEV_COMPOSE) exec backend python manage.py migrate

dev-seed:
	$(DEV_COMPOSE) exec backend python manage.py seed_dev

dev-test:
	$(DEV_COMPOSE) exec backend pytest tests/ -v

# ============================================================================
# PROD/STAGING DOCKER
# ============================================================================

prod-build:
	$(PROD_COMPOSE) build

prod-up:
	$(PROD_COMPOSE) up -d --build

prod-down:
	$(PROD_COMPOSE) down

prod-logs:
	$(PROD_COMPOSE) logs -f

prod-seed:
	$(PROD_COMPOSE) exec backend python manage.py seed_prod
