# Docs Sync

Keep `docs/API.md` in sync with the live OpenAPI spec.

## Steps

1. Fetch the current OpenAPI spec:
   - Read `http://localhost:8000/openapi.json` using WebFetch
   - If the server is not running, tell the user to run `make run` first and stop

2. Read the existing `docs/API.md` (if it exists)

3. Compare routes:
   - List routes present in OpenAPI but **missing** from `docs/API.md` → **added**
   - List routes documented in `docs/API.md` but **absent** from OpenAPI → **removed**
   - List routes present in both but with mismatched parameters or response schemas → **changed**

4. Rewrite `docs/API.md` to reflect the current OpenAPI spec:
   - One section per router tag (e.g. `notes`, `action-items`)
   - For each endpoint: method, path, summary, request body fields, response fields
   - Keep any hand-written notes/examples that don't conflict

5. Output a diff-like summary and a TODO list

## Output Format

```
Routes added   (+): POST /notes/{id}/extract
Routes removed (-): (none)
Routes changed (~): GET /notes — response schema updated

docs/API.md updated ✅

TODOs:
  - Add integration test for POST /notes/{id}/extract
  - Update frontend to call new endpoint
```
