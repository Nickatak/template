# ADR 0001: Template Runtime Modes and Command Taxonomy

- Status: Accepted
- Date: 2026-02-21
- Decision Owners: Template Maintainer

## Context

This repository is intended to be a fast starting point for "I need an app that
does X." The template needs to work immediately as a standalone app while also
fitting a parent orchestration model used by multi-app host deployments.

Historically, Docker-oriented commands used a `dev-*` prefix. In practice, that
name conflated environment intent ("development") with runtime mechanism
("Docker"), which caused ambiguity in workflows and documentation.

## Decision Drivers

- Keep day-1 setup and iteration fast for standalone use.
- Preserve compatibility with parent orchestration patterns.
- Make command semantics explicit and predictable.
- Enforce clearer env contracts for local, Docker, and production-like flows.

## Decisions

### 1. Runtime command taxonomy

Use exactly three runtime prefixes:

- `local-*`: host-native development flow.
- `docker-*`: Docker runtime flow.
- `prod-*`: production-like Docker flow.

`dev-*` command names are removed as a breaking change.

### 2. Dual-mode deployment support

The template remains runnable standalone but is also orchestration-ready:

- Base compose supports direct local Docker runs.
- Optional edge override supports parent orchestration patterns without app code
  changes.

### 3. Edge override pattern

`docker-compose.edge.yml` exists as an additive override for orchestration:

- strips host-exposed ports from app services
- joins shared external `edge` network
- provides stable network aliases for ingress routing

### 4. Environment contract validation

Env validation targets enforce required variables by mode:

- `env-validate-local`
- `env-validate-docker`
- `env-validate-prod`

This keeps startup failures early and explicit.

## Consequences

### Positive

- Clear distinction between runtime mode and environment intent.
- Better onboarding consistency across repos.
- Easier integration into host-level deploy orchestration.

### Tradeoffs

- Breaking command changes require users to update muscle memory and scripts.
- Slightly more documentation and Makefile surface area to maintain.

## Implementation Notes

- Makefile command groups were renamed and reorganized.
- New env validation script was added at `scripts/validate-env.sh`.
- README was rewritten to reflect the new runtime contract.
- `.env.example` now includes explicit `STAGING_*` contract keys.
