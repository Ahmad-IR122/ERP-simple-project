# Preflight Check

## Purpose

Run all important project validation checks before pushing code or opening a Pull Request.

Use this skill when the user asks to:

- Check the project before push
- Validate backend changes
- Validate frontend changes
- Validate Docker configuration
- Verify CI readiness
- Prepare code for a Pull Request

## Project Stack

Backend:
- FastAPI
- Python
- SQLAlchemy
- Alembic
- Supabase PostgreSQL
- Clerk
- Pytest
- Ruff

Frontend:
- React
- Vite
- TypeScript

Infrastructure:
- Docker
- Docker Compose
- GitHub Actions

## General Rules

Before running checks:

1. Inspect the current Git status.
2. Detect which parts of the project changed.
3. Run only the relevant checks unless the user asks for a full validation.
4. Do not modify unrelated files.
5. Do not commit or push unless explicitly requested.
6. Do not expose or print secrets from `.env` files.

## Backend Checks

If backend files changed, run from the backend directory:

```bash
ruff check .
python -m pytest
```

If Alembic migrations changed, also run:

```bash
alembic current
alembic heads
```

If database access is available and the user explicitly wants migration validation, run:

```bash
alembic upgrade head
```

Do not apply migrations automatically when there is any risk of destructive schema changes.

## Frontend Checks

If frontend files changed, run from the frontend directory:

```bash
npm run lint
npx tsc -b
npm run build
```

If package files changed, prefer:

```bash
npm ci
```

before validation.

## Docker Checks

If Docker-related files changed, run:

```bash
docker compose config
```

If Docker is available locally and the user asks for a full Docker validation, also run:

```bash
docker compose build
```

Do not run containers unnecessarily.

## Authentication Checks

If Clerk-related code changed, verify:

- Required Clerk environment variables exist
- No Clerk secret is exposed in frontend code
- Protected backend routes use the existing authentication dependency
- JWT verification configuration is still valid

Do not print JWTs or secrets.

## Database Checks

If Supabase or database code changed, verify:

- `DATABASE_URL` is referenced through environment configuration
- No credentials are committed
- SQLAlchemy imports work
- Alembic metadata loads correctly

## Git Checks

Before reporting success, run:

```bash
git status
```

Inspect changed files.

Warn if sensitive files are staged, including:

```text
.env
.env.local
*.pem
*.key
credentials.json
```

## Failure Handling

If any check fails:

1. Stop claiming the project is ready.
2. Identify the exact failing command.
3. Show the relevant error.
4. Explain the likely cause.
5. Fix only the relevant issue if requested.
6. Re-run the failed check after the fix.

## Success Criteria

A full preflight passes only when:

Backend:
- Ruff passes
- Pytest passes

Frontend:
- ESLint passes
- TypeScript check passes
- Vite build passes

Docker:
- Docker Compose config passes when Docker files are involved

Git:
- No sensitive files are staged

## Final Report

At the end report:

- Backend checks: PASS / FAIL / SKIPPED
- Frontend checks: PASS / FAIL / SKIPPED
- Docker checks: PASS / FAIL / SKIPPED
- Migration checks: PASS / FAIL / SKIPPED
- Sensitive file check: PASS / FAIL
- Overall status: READY or NOT READY

Do not report READY if any required check fails.
