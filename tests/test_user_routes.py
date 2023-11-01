# /tests/test_user_routes.py
from fastapi.testclient import TestClient

from main import app
from models import User

from .test_setup import (db_session, sample_department_roles,
                         sample_departments, sample_users)

client = TestClient(app)


def test_read_users(db_session, sample_users):
    response = client.get("/users/")
    assert response.status_code == 200

    response_users = response.json()
    assert len(response_users) >= len(sample_users)


def test_read_user(db_session, sample_users):
    test_user = sample_users[0]

    response = client.get(f"/user/{test_user.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(test_user.id)
    assert response.json()["name"] == test_user.name


def test_read_user_not_found(db_session):
    nonexistent_uuid = "123e4567-e89b-12d3-a456-426614174000"

    response = client.get(f"/user/{nonexistent_uuid}")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_user_wrong_format(db_session):
    wrong_format = "wrong"

    response = client.get(f"/user/{wrong_format}")

    assert response.status_code == 422
