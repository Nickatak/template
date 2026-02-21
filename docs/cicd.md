# CI/CD Blueprint

This template uses a blended good+mature CI/CD baseline:

- Orchestration-aware artifact publishing
- Security scans on source and images
- Promotion model using immutable image digests

## Workflows

- `.github/workflows/ci.yml`
  - Runs on PR and `master` pushes
  - Validates env contracts (`local`, `docker`, `prod`)
  - Runs backend tests (`make local-test`, non-E2E default)
  - Runs frontend lint/build
  - Renders compose contracts (`docker`, `edge`, `prod`)
  - Smoke-builds backend/frontend Docker images
  - Runs gitleaks + Trivy filesystem critical scan

- `.github/workflows/publish-images.yml`
  - Runs on `master` push and manual dispatch
  - Builds and pushes backend/frontend images to GHCR
  - Produces digest-pinned image refs
  - Attests build provenance
  - Uploads `release-manifest.json` artifact
  - Scans pushed images with Trivy (critical)

- `.github/workflows/promote.yml`
  - Manual promotion request (`staging`/`production`)
  - Requires digest-pinned image refs
  - Emits `deployment-intent.json` artifact
  - Optionally dispatches event to parent orchestration repo

## Required Repository Configuration

### Permissions

- Actions must have permission to write packages (`publish-images.yml`)

### Secrets and Variables

Optional for orchestration dispatch from `promote.yml`:

- Secret: `ORCHESTRATION_DISPATCH_TOKEN`
- Variable: `ORCHESTRATION_REPO` (format: `owner/repo`)

If unset, promotion still emits deployment intent artifact for manual pickup.

## Promotion Contract

Promotions must use immutable refs:

- `ghcr.io/<owner>/<repo>/backend@sha256:<digest>`
- `ghcr.io/<owner>/<repo>/frontend@sha256:<digest>`

Parent orchestration should consume these digests directly in Compose overrides or deployment manifests.
