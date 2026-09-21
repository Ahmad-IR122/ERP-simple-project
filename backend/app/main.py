from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text

from app.core.auth import get_current_user
from app.core.database import engine
from app.modules.products import router as products_router
from app.modules.users import router as users_router
from app.modules.users.models import User

app = FastAPI(
    title="Simple ERP API",
    version="1.0.0",
)

app.include_router(products_router)
app.include_router(users_router)


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
