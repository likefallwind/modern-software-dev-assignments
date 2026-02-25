# Tasks for Repo

## 1) Enable pre-commit and fix the repo
- Install hooks: `pre-commit install`
- Run: `pre-commit run --all-files`
- Fix any formatting/lint issues (black/ruff)

## 2) Add search endpoint for notes
- Add/extend `GET /notes/search?q=...` (case-insensitive) using SQLAlchemy filters
- Update `frontend/app.js` to use the search query
- Add tests in `backend/tests/test_notes.py`

## 3) Complete action item flow
- Implement `PUT /action-items/{id}/complete` (already scaffolded)
- Update UI to reflect completion (already wired) and extend test coverage

## 4) Improve extraction logic
- Extend `backend/app/services/extract.py` to parse tags like `#tag` and return them
- Add tests for the new parsing behavior
- (Optional) Expose `POST /notes/{id}/extract` that turns notes into action items

## 5) Notes CRUD enhancements
- Add `PUT /notes/{id}` to edit a note (title/content)
- Add `DELETE /notes/{id}` to delete a note
- Update `frontend/app.js` to support edit/delete; add tests

## 6) Request validation and error handling
- Add simple validation rules (e.g., min lengths) to `schemas.py`
- Return informative 400/404 errors where appropriate; add tests for validation failures

## 7) Docs drift check (manual for now)
- Create/maintain a simple `API.md` describing endpoints and payloads
- After each change, verify docs match actual OpenAPI (`/openapi.json`)

---

## TestAgent Hand-off Notes (2026-02-25)

### Test Coverage Expansion

**Starting state:** 15 tests passing across 3 files.
**Ending state:** 35 tests passing across 3 files.

### Tests added (20 new tests):

#### `backend/tests/test_action_items.py` (+4 tests)
- `test_complete_action_item_not_found` - PUT /action-items/9999/complete returns 404
- `test_list_action_items_empty` - GET /action-items/ on empty DB returns []
- `test_list_action_items_multiple` - GET /action-items/ returns all items when multiple exist
- `test_complete_item_fields` - PUT /complete returns all expected fields (id, description, completed)

#### `backend/tests/test_notes.py` (+11 tests)
- `test_get_note_by_id` - GET /notes/{id} returns the correct note
- `test_get_note_by_id_not_found` - GET /notes/9999 returns 404
- `test_update_note_only_content` - PUT /notes/{id} with only content updates content, preserves title
- `test_update_note_both_fields` - PUT /notes/{id} with both fields updates both
- `test_search_empty_q_returns_all` - GET /notes/search/?q="" returns all notes
- `test_search_no_match_returns_empty` - GET /notes/search/?q=... returns [] when nothing matches
- `test_search_matches_title` - Case-insensitive search hits note titles
- `test_search_matches_content` - Case-insensitive search hits note contents
- `test_delete_note_makes_it_unfetchable` - After DELETE, GET returns 404
- `test_extract_returns_empty_lists_for_plain_text` - /extract on plain text returns empty lists

#### `backend/tests/test_extract.py` (+7 tests)
- `test_extract_empty_text` - Empty string returns empty action_items and tags
- `test_extract_no_action_items` - Plain sentence yields no action items
- `test_extract_action_item_exclamation` - Lines ending in ! are captured
- `test_extract_action_item_todo_case_insensitive` - TODO: prefix lines are captured
- `test_extract_returns_dict_keys` - Return value always has action_items and tags keys
- `test_extract_multiple_tags` - Multiple #tags in one string all captured

### Gaps still open (for CodeAgent if needed)
- `NoteUpdate` schema does not enforce min_length on optional fields; an update payload of
  `{"title": ""}` currently succeeds with 200 (not 422). If validation is desired, add
  `min_length=1` to `NoteUpdate.title` / `NoteUpdate.content` and add matching tests.
- No test for the `GET /notes/` list endpoint isolation (empty DB returns []).
- No test verifying the note `id` field is an integer in the response body.
