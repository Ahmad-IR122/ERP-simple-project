from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine
from app.modules.products import router as products_router

app = FastAPI(
    title="Simple ERP API",
    version="1.0.0",
)

app.include_router(products_router)


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