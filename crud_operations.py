# crud_operations.py
from uuid import UUID

from sqlalchemy.orm import Session, aliased

import models
import schemas as schema
from security import hash_password

"""
CRUD operations for the database.
"""


def create_user(db: Session, user: schema.UserCreate):
    default_password = "123456789"  # using common password for demo purposes
    hashed_password = hash_password(default_password)
    db_user = models.User(name=user.name, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return None


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()


def update_user(db: Session, user: schema.User):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Department).offset(skip).limit(limit).all()


def get_department_by_name(db: Session, department_name: str):
    return (
        db.query(models.Department)
        .filter(models.Department.name == department_name)
        .first()
    )


def get_department_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.DepartmentRole).offset(skip).limit(limit).all()


def get_department_by_id(db: Session, department_id: str):
    return (
        db.query(models.Department)
        .filter(models.Department.id == department_id)
        .first()
    )


def get_department_role_by_id(db: Session, department_role_id: str):
    return (
        db.query(models.DepartmentRole)
        .filter(models.DepartmentRole.id == department_role_id)
        .first()
    )


def get_department_roles_by_department_id(db: Session, department_id: UUID):
    return (
        db.query(models.DepartmentRole)
        .filter(models.DepartmentRole.department_id == department_id)
        .all()
    )
