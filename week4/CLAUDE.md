# Claude Code Guidelines for Week 4 Project

## Code Navigation and Entry Points
- **App Entry Point:** The FastAPI application is centrally located and can be run using `make run` (which executes `uvicorn backend.app.main:app --reload`).
- **Routers:** All API endpoints and routers live in `backend/app/routers/`.
- **Tests:** All tests are located in `backend/tests/`. Run them using `make test`.
- **Database Seeding:** The database can be initialized and seeded with initial data by running `make seed`.

## Style and Safety Guardrails
- **Tooling Expectations:** We strictly use `black` for code formatting and `ruff` for linting. 
- **Lint/Test Gates:** Before committing any code or finalizing a feature, you **must** verify it passes the linters and tests.
- **Safe Commands:** `make run`, `make test`, `make format`, `make lint`, and `make seed` are safe to run anytime.
- **Commands to Avoid:** Do not manually modify `.sqlite` database files directly or bypass the `make` utility for routine scripts. Always prefer using the provided Makefile commands.

## Workflow Snippets
- **Adding a New Endpoint:**
  1. First, write a failing test in `backend/tests/`.
  2. Implement the endpoint in `backend/app/routers/`.
  3. Run `make test` to ensure it passes.
  4. Run `make format` and `make lint` to adhere to code styles.
- **Refactoring:** Utilize the custom `/refactor-module` command if renaming modules to safely update imports and verify tests.
