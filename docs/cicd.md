# CI/CD Blueprint

This repo uses a blended good+mature CI/CD model:

- strict validation on PR/push (`CI`)
- immutable artifact publishing (`Publish Images`)
- explicit promotion contract for parent orchestration (`Promote Release`)

## Workflow Overview

### `ci.yml`

Purpose: authoritative quality gate before merge/deploy.

- Trigger:
  - pull requests
  - push to `master`
- Checks:
  - env contract validation (`local`, `docker`, `prod`)
  - backend tests (`make local-test`, non-E2E default)
  - frontend lint/build
  - compose render checks (`docker`, `edge`, `prod`)
  - docker smoke build (backend/frontend)
  - gitleaks + Trivy filesystem critical scan

### `publish-images.yml`

Purpose: build/push immutable deploy artifacts.

- Trigger:
  - push to `master`
  - manual (`workflow_dispatch`)
- Outputs:
  - GHCR images for backend/frontend
  - digest-pinned refs (`...@sha256:...`)
  - provenance attestations
  - `release-manifest.json` artifact
  - image-level Trivy critical scan

### `promote.yml`

Purpose: emit promotion intent for parent orchestration.

- Trigger:
  - manual (`workflow_dispatch`)
- Inputs:
  - `environment`: `staging` or `production`
  - `backend_image`: digest-pinned GHCR ref
  - `frontend_image`: digest-pinned GHCR ref
- Behavior:
  - rejects non-digest refs
  - emits `deployment-intent.json`
  - optionally dispatches `repository_dispatch` to orchestration repo

## Initial Setup

### 1) Repository Actions Permissions

In GitHub repo settings:

- `Actions` -> `General` -> `Workflow permissions`
  - set to `Read and write permissions` (needed for GHCR publish/attestation)

### 2) Optional Orchestration Dispatch

Set only if parent repo should be auto-notified from `promote.yml`:

- repo secret: `ORCHESTRATION_DISPATCH_TOKEN`
- repo variable: `ORCHESTRATION_REPO` (`owner/repo`)

If these are unset, promotion still works and uploads `deployment-intent.json` for manual pickup.

### 3) Branch Protection (Recommended)

Protect `master` and require at least:

- `CI / Contracts, Tests, and Build`
- `CI / Security Scan`

Also recommended:

- require PR review
- block direct pushes to `master`

## Day-to-Day Usage

### Validate a PR

1. Open PR against `master`.
2. Wait for `CI` workflow to complete.
3. Merge only when all required checks pass.

### Publish images

Automatic:

- merge/push to `master` triggers `Publish Images`.

Manual:

1. GitHub -> Actions -> `Publish Images` -> `Run workflow`.
2. Choose branch (usually `master`).

Get published digest refs from:

- workflow logs (`backend_image` / `frontend_image`)
- `release-manifest.json` artifact

### Promote a release

1. GitHub -> Actions -> `Promote Release` -> `Run workflow`.
2. Input:
   - environment (`staging` or `production`)
   - digest-pinned backend/frontend refs
3. Download/inspect `deployment-intent.json`.
4. Parent orchestration consumes that intent or receives dispatch automatically (if configured).

## Promotion Contract

Only immutable refs are accepted:

- `ghcr.io/<owner>/<repo>/backend@sha256:<digest>`
- `ghcr.io/<owner>/<repo>/frontend@sha256:<digest>`

Tag refs like `:latest` are rejected by design.

## Pipeline Shakedown Checklist

Use this once when bootstrapping or changing workflows:

1. Create a PR with harmless change -> verify `CI` runs.
2. Introduce an intentional failure -> verify `CI` fails.
3. Revert/fix -> verify `CI` goes green.
4. After merge to `master`, run `Publish Images` and confirm:
   - images pushed
   - manifest artifact uploaded
5. Run `Promote Release` once:
   - invalid tag ref should fail
   - valid digest refs should pass

Note: `workflow_dispatch` workflows are only invokable once they exist on the repository's default branch.

## Troubleshooting

- `gitleaks` revision error on PR:
  - ensure checkout uses full history (`fetch-depth: 0`) in scan job.
- Trivy critical failures:
  - patch vulnerable dependencies and rerun.
- Docker smoke build fails in frontend:
  - ensure Dockerfile copy targets (for example `public/`) actually exist.
- Promotion dispatch not firing to parent:
  - confirm `ORCHESTRATION_DISPATCH_TOKEN` and `ORCHESTRATION_REPO` are set.
