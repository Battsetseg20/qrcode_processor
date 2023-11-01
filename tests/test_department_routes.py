from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app
from models import Department
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


def test_read_departments(client, db_session):
    response = client.get("/departments/")
    assert response.status_code == 200
    assert any(
        [department["name"] == "TestDepartment" for department in response.json()]
    )


def test_read_department(client, db_session, sample_department):
    response = client.get(f"/department/{sample_department.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestDepartment"


def test_delete_department_user_is_not_admin(
    client, test_user_jwt_token, db_session, sample_department
):
    department_id = sample_department.id
    response = client.delete(
        f"/department/{department_id}",
        headers={"Authorization": f"Bearer { test_user_jwt_token}"},
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "User does not have an admin permission for this department"
    }


def test_delete_department_department_not_found(
    client, test_user_jwt_token, db_session, sample_department
):
    department_id = uuid4()
    response = client.delete(
        f"/department/{department_id}",
        headers={"Authorization": f"Bearer { test_user_jwt_token}"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Department not found"}
