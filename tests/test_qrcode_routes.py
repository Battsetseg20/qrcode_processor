import os
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt

from main import app
from models import Base, Department, DepartmentRole, User
from security import ALGORITHM, create_access_token

from .test_setup import (db_session, sample_department,
                         sample_department_roles, sample_departments,
                         sample_user, sample_users)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def test_user_jwt_token(sample_user):
    return create_access_token(data={"sub": sample_user.name})


def test_upload_qr(client, test_user_jwt_token, db_session):
    with open("./test_qrcodes/update_dept_qr.png", "rb") as qr_file:
        response = client.post(
            "/upload_qr/",
            files={"file": qr_file},
            headers={"Authorization": f"Bearer {test_user_jwt_token}"},
        )
    assert response.status_code == 200
    assert "detail" in response.json()
    assert response.json()["detail"] == "QR code processed"


def test_upload_qr_invalid_data(client, test_user_jwt_token, db_session):
    with open("./test_qrcodes/unprocessable_qr.png", "rb") as qr_file:
        response = client.post(
            "/upload_qr/",
            files={"file": qr_file},
            headers={"Authorization": f"Bearer {test_user_jwt_token}"},
        )
    assert response.status_code == 500
    assert "detail" in response.json()
    assert (
        response.json()["detail"]
        == "Error processing QR code: badly formed hexadecimal UUID string"
    )


def test_upload_qr_without_auth(client, test_user_jwt_token, db_session):
    with open("./test_qrcodes/update_dept_qr.png", "rb") as qr_file:
        response = client.post(
            "/upload_qr/", files={"file": qr_file}, headers={"Authorization": ""}
        )
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Not authenticated"


def test_upload_qr_invalid_jwt_token(client):
    # Create a token with a different secret key
    wrong_secret_key = "wrong-secret-key"
    invalid_token = jwt.encode(
        {"sub": "testuser"}, wrong_secret_key, algorithm=ALGORITHM
    )

    with open("./test_qrcodes/update_dept_qr.png", "rb") as qr_file:
        response = client.post(
            "/upload_qr/",
            files={"file": qr_file},
            headers={"Authorization": f"Bearer {invalid_token}"},
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
