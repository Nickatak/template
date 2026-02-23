# Frontend Architecture Map Template

## Purpose
State how this frontend organizes route composition, feature boundaries, and debug trace flow.

## Layer Rules
1. `app/**/page.tsx` contains route composition only.
2. `features/<feature>/components/*` contains feature UI.
3. `features/<feature>/api.ts` contains endpoint calls only.
4. `features/<feature>/types.ts` contains transport and domain shapes.
5. Policy-contract adapters live in `features/<feature>/contracts/*` when applicable.
6. Shared cross-feature helpers live under `features/shared/*`.

## Route Shim Policy
1. Route files under `app/**/page.tsx` are URL shims only.
2. Route files should mount feature entries and provide layout framing.
3. Route files should not contain domain mutation logic, validation flow, or API orchestration.
4. Move branching workflow behavior into feature-level components/controllers.

## Route To Entry Map
| Route | Route File | Primary Entry |
| --- | --- | --- |
| `/example` | `frontend/app/example/page.tsx` | `frontend/features/example/components/example-console.tsx` |
| `/demo-feature` | `frontend/app/demo-feature/page.tsx` | `frontend/features/demo-feature/components/demo-feature-console.tsx` |

## Redirect Routes
| Route | Redirect Behavior |
| --- | --- |
| `/example-shortcut` | redirects to canonical route |

## Workflow Contract Features
List features that consume backend policy-contract endpoints.

1. `feature-name` -> `GET /contracts/<feature>/`

## Debug Trace Protocol
1. Start in route file under `app/**/page.tsx`.
2. Follow imported feature entry component.
3. Open `frontend/features/<feature>/FEATURE_MAP.md`.
4. Check contract adapter/state map.
5. Check API request payload and response handling.
6. Return to component rendering logic last.

## Feature Map Coverage
List all feature map files in this project.

1. `frontend/src/features/<feature>/FEATURE_MAP.md`
2. `frontend/features/demo-feature/FEATURE_MAP.md` (included example)
3. Template: `frontend/FEATURE_MAP_TEMPLATE.md`
