---
description: "Run the project's tests, lint, and build checks. Optionally scope to one suite, e.g. /test backend."
argument-hint: "[suite]"
---

Run this project's validation checks.

1. **Find the commands.** Use the test / lint / build commands documented in `CLAUDE.md` (e.g. a "Validation" or "Dev commands" section). If none are documented, detect them from the project, e.g. `uv run pytest` / `pytest` (Python), `npm run lint` / `npm run build` (Node), `cargo test` (Rust), `go test ./...` (Go), and note what you ran.
2. **Scope (optional).** `$ARGUMENTS` may name a suite (e.g. `backend`, `frontend`, `unit`) to run only that subset; with no argument, run all of them.
3. **Run** each command, capturing pass/fail counts and any failure details.
4. **Report** a clear pass/fail status per step. For failures, include the file, line number, and error message.

> Example for a split repo (adapt to your project): `cd backend && uv run pytest -v` for the API; `cd frontend && npm run lint && npm run build` for the UI.
