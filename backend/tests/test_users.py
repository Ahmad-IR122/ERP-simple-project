from uuid import UUID

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
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def user_payload(**overrides):
    payload = {
        "clerk_user_id": "user_123",
        "email": "person@example.com",
        "first_name": "Ada",
        "last_name": "Lovelace",
    }
    payload.update(overrides)
    return payload


def test_create_list_get_update_and_delete_user():
    create_response = client.post("/users", json=user_payload())

    assert create_response.status_code == 201
    user = create_response.json()
    assert UUID(user["id"])
    assert user["role"] == "employee"
    assert user["created_at"]
    assert user["updated_at"]

    list_response = client.get("/users")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/users/{user['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "person@example.com"

    update_response = client.patch(
        f"/users/{user['id']}",
        json={"role": "manager", "first_name": "Grace"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["role"] == "manager"
    assert update_response.json()["first_name"] == "Grace"

    delete_response = client.delete(f"/users/{user['id']}")
    assert delete_response.status_code == 204
    assert client.get(f"/users/{user['id']}").status_code == 404


def test_duplicate_clerk_user_id_and_email_are_rejected():
    assert client.post("/users", json=user_payload()).status_code == 201

    duplicate_clerk_id = client.post(
        "/users", json=user_payload(email="other@example.com")
    )
    assert duplicate_clerk_id.status_code == 409

    duplicate_email = client.post(
        "/users", json=user_payload(clerk_user_id="user_456")
    )
    assert duplicate_email.status_code == 409


def test_missing_required_fields_are_rejected():
    response = client.post("/users", json={"email": "person@example.com"})

    assert response.status_code == 422


def test_missing_user_returns_not_found():
    response = client.get("/users/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
