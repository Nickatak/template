# Edge Orchestration Mode

This template supports two runtime modes:

- Standalone mode: app services publish host ports directly.
- Edge mode: app services are private, and traffic is routed through a parent
  ingress/reverse-proxy stack.

`docker-compose.edge.yml` is the switch for edge mode.

## What The Edge Override Changes

When layered on top of `docker-compose.yml`, it:

- removes host port publishing for `mysql`, `backend`, and `frontend`
- attaches `backend` and `frontend` to an external Docker network named `edge`
- adds stable aliases on that network:
  - `template-backend`
  - `template-frontend`

## Why This Exists

This pattern keeps app repos deploy-agnostic while letting a parent orchestration
repo own host/domain/ingress concerns. The app can run standalone or be composed
into a shared host ingress model without code changes.

## Parent Repo Usage Pattern

A parent repo can run this template with:

```bash
docker compose \
  -f /path/to/template/docker-compose.yml \
  -f /path/to/template/docker-compose.edge.yml \
  --env-file /path/to/parent/env/template.staging.env \
  up -d
```

Then the parent ingress proxy can route internally, for example:

- `/` -> `http://template-frontend:3000`
- `/api` -> `http://template-backend:8000`

## Local Verification

Use:

```bash
make docker-edge-network
make docker-edge-config
```

`docker-edge-config` should show:

- no `ports:` entries for app services
- `edge` network attachments with expected aliases

## Notes

- `edge` network must already exist (`docker network create edge`).
- Host/origin policy should be controlled via env:
  - `DOCKER_ALLOWED_HOSTS`
  - `DOCKER_CORS_ALLOWED_ORIGINS`
  - `DOCKER_CSRF_TRUSTED_ORIGINS`
