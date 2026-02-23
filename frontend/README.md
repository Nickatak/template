# Frontend Mapping Templates

## Files
1. `FEATURE_MAP_TEMPLATE.md` - per-feature debug and composition map template.
2. `ARCHITECTURE_MAP_TEMPLATE.md` - global route/layer/dependency map template.

## Usage
1. Copy `ARCHITECTURE_MAP_TEMPLATE.md` into your project root as `frontend/ARCHITECTURE_MAP.md`.
2. Copy `FEATURE_MAP_TEMPLATE.md` into `frontend/features/` (or keep it in `frontend/` as a root template reference).
3. Create `FEATURE_MAP.md` in each feature directory and fill purpose, route surface, mutation map, composition/entry flow, API surface, contracts, state model, error/empty states, and test anchors.
4. Use `frontend/app/demo-feature/page.tsx` + `frontend/features/demo-feature/*` as the canonical route-shim -> feature-parent example.

## Route Shim Policy
1. Treat `app/**/page.tsx` as URL-to-feature shims.
2. Keep route files focused on layout/composition and feature entry mounting.
3. Keep workflow logic, API orchestration, and validation inside `features/<feature>/`.
