from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.auth import get_current_user
from app.core.database import engine
from app.modules.products import router as products_router
from app.modules.users import router as users_router
from app.modules.users.models import User
from app.webhooks.clerk import router as clerk_webhook_router
from app.core.permissions import require_role

app = FastAPI(
    title="Simple ERP API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(users_router)
app.include_router(clerk_webhook_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
  
@app.get("/health/db")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
    
@app.get("/me")
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return {
        "id": current_user.id,
        "clerk_user_id": current_user.clerk_user_id,
        "email": current_user.email,
        "role": current_user.role,
    }

@app.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_role("admin")),
):
    return {
        "message": "Admin access granted",
        "email": current_user.email,
        "role": current_user.role,
    }
    
@app.get("/employee-test")
def employee_test(
    current_user: User = Depends(require_role("employee")),
):
    return {
        "message": "Employee access granted",
        "email": current_user.email,
        "role": current_user.role,
    }