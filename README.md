# Template Repository

Full-stack starter template with JWT auth, user management, and a protected
dashboard flow. Backend is Django REST Framework, frontend is Next.js.

## Breaking Change

Environment command taxonomy is now:

- `local-*` for host-native workflows
- `docker-*` for Docker workflows
- `prod-*` for production-like Docker workflows

`dev-*` command names were intentionally removed.

Rationale is documented in `docs/adr/0001-template-runtime-and-command-taxonomy.md`.

## Goals

- Fast standalone startup for new apps
- Clean path to deploy orchestration via Compose overrides
- Clear environment contracts for local, docker, and prod modes

## Features

- JWT login/register/logout/me endpoints
- Email-based custom user model
- Protected dashboard routing
- Backend/frontend separation with API-first design
- Docker stack with MySQL runtime defaults

## Prerequisites

- Python 3.8+
- Node.js 16+
- Make
- Docker (for `docker-*` / `prod-*` flows)

## Environment Configuration

This repo uses `.env` as a symlink to mode-specific files:

- `.env.dev`
- `.env.prod`
- `.env.example` (template)

Initialize env files once:

```bash
make env-init
```

Switch active env:

```bash
./scripts/toggle-env.sh dev
./scripts/toggle-env.sh prod
./scripts/toggle-env.sh current
```

Validate env contract:

```bash
make env-validate-local
make env-validate-docker
make env-validate-prod
```

`make env-validate-prod` will fail on a fresh clone until production-like
variables are set in `.env.prod`.

Common host/origin overrides:

- `DOCKER_ALLOWED_HOSTS`
- `DOCKER_CORS_ALLOWED_ORIGINS`
- `DOCKER_CSRF_TRUSTED_ORIGINS`
- `STAGING_ALLOWED_HOSTS`
- `STAGING_CORS_ALLOWED_ORIGINS`
- `STAGING_CSRF_TRUSTED_ORIGINS`

## Quickstart

```bash
make local-install
make local-up
```

- Backend API: `http://localhost:8000/api/`
- Frontend: `http://localhost:3000/`

## Command Groups

### Local

- `make local-install`
- `make local-up`
- `make local-run-backend`
- `make local-run-frontend`
- `make local-kill-ports`
- `make local-test`
- `make local-test-api`
- `make local-test-e2e`
- `make local-test-cov`
- `make local-migrate`
- `make local-seed`
- `make local-pre-commit-install`
- `make local-clean`

### Docker

- `make docker-build`
- `make docker-up`
- `make docker-down`
- `make docker-logs`
- `make docker-shell-backend`
- `make docker-shell-mysql`
- `make docker-migrate`
- `make docker-seed`
- `make docker-test`
- `make docker-config`

Docker defaults to MySQL:
`DATABASE_URL=mysql://template:template@mysql:3306/template`

### Production-Like

- `make prod-build`
- `make prod-up`
- `make prod-down`
- `make prod-logs`
- `make prod-seed`

Uses:

- `docker-compose.yml`
- `docker-compose.staging.yml`

## Standalone and Orchestration-Ready

This repo runs standalone by default. It is also orchestration-ready by using
Compose override layering.

Optional edge override:

- `docker-compose.edge.yml` removes host port publishing for app services
- attaches services to external `edge` network
- adds stable aliases: `template-frontend`, `template-backend`
- full walkthrough: `docs/edge-orchestration.md`

Example:

```bash
make docker-edge-network
make docker-edge-up
```

Render effective config:

```bash
make docker-edge-config
make prod-config
```

## CI/CD

This template includes a blended good+mature CI/CD baseline with:

- PR/push validation pipeline
- Immutable image publishing to GHCR
- Security scans on source and published images
- Manual promotion contract for parent orchestration

See `docs/cicd.md` for workflow details and required repo settings.

## Project Structure

```text
├── backend/                      # Django backend project
│   ├── api/                      # Django app
│   ├── core/                     # Django project settings
│   ├── tests/                    # Backend test suite
│   ├── manage.py                 # Django CLI entry
│   └── requirements.txt          # Backend Python deps
├── frontend/                     # Next.js app
├── scripts/                      # Env + utility scripts
├── docker-compose.yml            # Base compose
├── docker-compose.staging.yml    # Production-like override
├── docker-compose.edge.yml       # Orchestration-ready edge override
└── Makefile                      # Command entry points
```

## Authentication Endpoints

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
