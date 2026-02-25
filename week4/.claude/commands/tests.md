# Run Tests with Coverage

Run the test suite for the week4 backend. If all tests pass, also run coverage and report results.

## Steps

1. Run: `PYTHONPATH=. pytest -q backend/tests --maxfail=1 -x`
2. If tests fail:
   - Show the failing test name and error message
   - Suggest a likely fix based on the failure
3. If tests pass:
   - Run: `PYTHONPATH=. pytest --cov=backend backend/tests`
   - Summarize total coverage % per module
   - Highlight any module below 80% coverage and suggest what to test next

## Output Format

```
✅ Tests passed  (or ❌ X tests failed)

Coverage summary:
  backend/app/routers/notes.py       92%
  backend/app/routers/action_items.py 78%
  backend/app/services/extract.py    65%  ← needs more tests

Next steps: ...
```
