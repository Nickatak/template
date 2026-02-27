# Auth Gate Pattern (Next.js App Router)

## Purpose

Centralize authentication checks and route protection so pages do not each implement their own token/redirect logic.

This pattern prevents auth flicker and stale-tab redirects by combining:

1. Shared client session storage with change events.
2. A single session-authorization verifier (`/auth/profile/`).
3. A route-level `AuthGate` that decides render/redirect behavior.

## Files

1. `frontend/features/session/client-session.ts`
2. `frontend/features/session/use-shared-session.ts`
3. `frontend/features/session/session-authorization.tsx`
4. `frontend/features/session/public-routes.ts`
5. `frontend/app/auth-gate.tsx`
6. `frontend/app/layout.tsx`

## Flow

1. Login/register writes token via `saveClientSession(...)`.
2. `useSharedSessionAuth()` subscribes to localStorage + custom session change events.
3. `SessionAuthorizationProvider` verifies the token with `GET /auth/profile/`.
4. `AuthGate` behavior:
   - Public auth routes (`/login`, `/register`):
     - allow render
     - if already authorized, redirect to `/dashboard`
   - Protected routes:
     - show loading state while checking
     - redirect unauthorized users to `/login`
     - render children only when authorized

## Why This Is Reusable

1. Token storage and token verification are isolated from feature pages.
2. Redirect logic is centralized and testable in one component.
3. Session changes in one tab propagate to other tabs through the shared event/store subscription.
4. API helpers can read tokens from one source (`loadClientSession`) instead of direct localStorage key usage.

## Integration Checklist

- [ ] Add session storage helpers (`client-session.ts`) with save/load/clear + event dispatch.
- [ ] Add `useSharedSessionAuth()` with `useSyncExternalStore`.
- [ ] Add `SessionAuthorizationProvider` that verifies token against backend profile/me endpoint.
- [ ] Add `isPublicAuthRoute(...)` route matcher.
- [ ] Add `AuthGate` and wrap app layout children with provider + gate.
- [ ] Remove page-level token redirect checks and rely on gate behavior.
- [ ] Update API token getters/setters to use shared session helpers.
- [ ] Verify with `npm run lint` and `npm run build`.

## Notes

1. `session-authorization.tsx` intentionally treats transient network failures as non-forced logout to avoid unnecessary session drops during short upstream/CDN incidents.
2. Unauthorized statuses (`401`, `403`) clear local session and transition to `unauthorized`.
