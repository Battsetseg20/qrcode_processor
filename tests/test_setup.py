import os
from uuid import uuid4

import pytest
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Department, DepartmentRole, User

os.environ["DATABASE_URL"] = "postgresql://localhost/qrcode_processor_db_test"

from database import Base

engine = create_engine(os.environ["DATABASE_URL"])


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    db.commit()

    yield db

    db.close()


@fixture(scope="module")
def sample_users(db_session):
    users = [
        User(name="Sample User 1", hashed_password="password"),
        User(name="Sample User 2", hashed_password="password"),
        User(name="Sample User 3", hashed_password="password"),
    ]
    db_session.add_all(users)
    db_session.commit()
    return users


@fixture(scope="module")
def sample_departments(db_session):
    departments = [
        Department(id=uuid4(), name="Engineering"),
        Department(id=uuid4(), name="HR"),
    ]
    for department in departments:
        db_session.add(department)
    db_session.commit()
    return departments


@fixture(scope="module")
def sample_department_roles(db_session, sample_users, sample_departments):
    department_roles = []
    for i, user in enumerate(sample_users):
        department = sample_departments[0]

        role = "admin" if i == 0 else "member"  # First user is an admin

        department_role = DepartmentRole(
            user_id=user.id, department_id=department.id, role=role
        )

        department_roles.append(department_role)
        db_session.add(department_role)

    try:
        db_session.commit()
        print("Successfully committed department roles")
    except Exception as e:
        print(f"Error committing department roles: {e}")
        db_session.rollback()

    return department_roles


@pytest.fixture(scope="module")
def sample_user(db_session):
    print("sample_user started")
    user = User(name="TestUser", hashed_password="test_password")
    db_session.add(user)
    db_session.commit()
    print("sample_user completed")
    return user


@pytest.fixture(scope="module")
def sample_department(db_session):
    department = Department(name="TestDepartment")
    db_session.add(department)
    db_session.commit()
    return department


@pytest.fixture(scope="module")
def sample_department_role(db_session, sample_user, sample_department):
    role = UserDepartmentRole(
        user_id=sample_user.id, department_id=sample_department.id, role="member"
    )
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture(scope="function")
def rollback_db_session(db_session):
    yield db_session
    db_session.rollback()
