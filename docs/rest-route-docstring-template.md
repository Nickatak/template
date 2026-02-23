# REST Route Contract Docstring Template

Use this docstring format for DRF function routes (`@api_view`) and ViewSet
actions (`@action`). It is enforced by:

- `python3 scripts/check_route_docstrings.py`
- `make local-check-route-docstrings`

## Required sections

Every route docstring must include:

- `Contract:`
- `- Preconditions:`
- `- Object mutations:`
- `- Idempotency and retry semantics:`
- `- Test anchors:`

If the route supports `POST`, `PUT`, or `PATCH`, include:

- `- Incoming payload (...) shape:`

Guarantee lines must carry a source tag:

- `[DB]` for DB-level enforcement only
- `[APP]` for application-level enforcement only
- `[DB+APP]` for layered enforcement

## Copy/paste template

```python
"""<One-line intent summary>.

Contract:
- `GET`:
  - `200`: <success meaning>.
    - Guarantees: <state/response guarantee>. `[APP]`
  - `401`: <auth failure meaning>.
    - Guarantees: no object mutations. `[APP]`
- `POST`:
  - `201`: <creation success meaning>.
    - Guarantees:
      - <guarantee #1>. `[DB+APP]`
      - <guarantee #2>. `[APP]`
  - `400`: <validation failure meaning>.
    - Guarantees: no durable partial mutation from failed request path. `[DB+APP]`

- Preconditions:
  - <auth/tenant/resource requirements>.

- Object mutations:
  - `GET`: none.
  - `POST`:
    - Creates:
      - Standard: <primary rows or `none`>.
      - Audit: <audit/event rows or `none`>.
    - Edits:
      - Standard: <edited rows or `none`>.
      - Audit: <edited audit rows or `none`>.
    - Deletes: <deleted rows or `none`>.

- Incoming payload (`POST`) shape:
  - JSON map:
    {
      "field_a": "type (required/optional)",
      "field_b": "type"
    }

- Idempotency and retry semantics:
  - `GET` is idempotent and read-only.
  - `POST` is <idempotent/not idempotent/conditionally idempotent>; retries <effect>.

- Test anchors:
  - `backend/tests/<test_module>.py::<TestClass>::<test_name>`
  - `backend/tests/<test_module>.py::<TestClass>::<test_name>`
"""
```
