from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_create_and_read_product():
    response = client.post(
        "/products",
        json={"name": "Keyboard", "sku": "KB-001", "price": "49.99"},
    )

    assert response.status_code == 201
    product = response.json()
    assert product["quantity"] == 0
    assert product["description"] is None

    read_response = client.get(f"/products/{product['id']}")
    assert read_response.status_code == 200
    assert read_response.json()["sku"] == "KB-001"


def test_duplicate_sku_is_rejected():
    payload = {"name": "Keyboard", "sku": "KB-001", "price": "49.99"}
    assert client.post("/products", json=payload).status_code == 201

    response = client.post("/products", json=payload)

    assert response.status_code == 409
