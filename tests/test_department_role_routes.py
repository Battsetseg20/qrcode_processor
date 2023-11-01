import pytest
from fastapi.testclient import TestClient

from main import app
from models import DepartmentRole

from .test_setup import (db_session, rollback_db_session,
                         sample_department_roles, sample_departments,
                         sample_users)


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_read_department_roles(
    client, db_session, sample_department_roles, rollback_db_session
):
    response = client.get("/department_roles/")
    assert response.status_code == 200
