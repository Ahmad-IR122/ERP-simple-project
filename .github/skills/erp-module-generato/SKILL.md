# ERP Module Generator

## Purpose

Generate new ERP backend modules for the FastAPI application using the existing project architecture and coding conventions.

Use this skill when the user asks to create a new ERP module such as:

* Employees
* Products
* Inventory
* Suppliers
* Customers
* Sales
* Purchases
* Categories
* Warehouses

## Project Stack

Backend:

* FastAPI
* Python
* SQLAlchemy
* Alembic
* Pydantic
* Supabase PostgreSQL
* Clerk Authentication
* Pytest
* Ruff

Frontend:

* React
* Vite
* TypeScript

Infrastructure:

* Docker
* Docker Compose
* GitHub Actions

## Instructions

Before creating a module, inspect the existing backend structure and reuse the current project conventions.

Do not create a new architecture if one already exists.

Keep database logic, API logic, schemas, and business logic separated.

Prefer reusable code and avoid duplicated logic.

## Module Structure

When creating a new module, follow this structure unless the existing project uses another convention:

```text
backend/
└── app/
    └── modules/
        └── <module_name>/
            ├── __init__.py
            ├── model.py
            ├── schema.py
            ├── service.py
            └── router.py
```

Tests should be created under:

```text
backend/
└── tests/
    └── <module_name>/
        └── test_<module_name>.py
```

## Model Rules

Use SQLAlchemy models.

Every main entity should normally contain:

```text
id
created_at
updated_at
```

Use UUID primary keys unless the project already uses another convention.

Use PostgreSQL-compatible data types.

Define indexes and unique constraints when appropriate.

Define relationships clearly.

Do not store Clerk passwords or authentication credentials in the application database.

If the entity belongs to a user, store the Clerk user ID as a reference.

## Schema Rules

Create separate Pydantic schemas when needed:

```text
<Entity>Create
<Entity>Update
<Entity>Response
```

Do not expose internal database fields unnecessarily.

Use optional fields correctly for update schemas.

## Service Rules

Business logic belongs in the service layer.

The router should not contain complex database logic.

Typical service functions include:

```text
create_<entity>
get_<entity>
get_<entities>
update_<entity>
delete_<entity>
```

Handle database errors clearly.

Do not silently ignore exceptions.

## Router Rules

Use FastAPI `APIRouter`.

Use REST-style endpoints.

Example:

```text
POST   /products
GET    /products
GET    /products/{id}
PATCH  /products/{id}
DELETE /products/{id}
```

Use correct HTTP status codes.

Examples:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
```

Protect private routes using the existing Clerk authentication dependency.

## Database Migration

Whenever the database schema changes:

Create an Alembic migration.

Review the generated migration before accepting it.

Do not automatically delete existing tables or columns unless explicitly requested.

## Tests

Create tests for the main module behavior.

At minimum test:

```text
create
list
get by id
update
delete
not found
validation errors
```

Add authentication tests when the endpoint is protected.

## Validation

After generating or modifying a backend module, run the available project checks.

Preferred checks:

```bash
ruff check .
pytest
```

If the project contains additional backend checks, run them too.

Do not report completion if tests or lint checks fail.

## Output

When completing a module, summarize:

1. Files created or modified.
2. API endpoints added.
3. Database changes.
4. Migration created.
5. Tests added.
6. Validation results.

## Example Request

User:

```text
Create a products module.

Fields:
name
sku
description
price
quantity
category_id
```

Expected behavior:

Create the SQLAlchemy model, Pydantic schemas, service layer, FastAPI router, Alembic migration, and tests.

Register the router with the main FastAPI application if needed.

Reuse the existing authentication and database dependencies.
