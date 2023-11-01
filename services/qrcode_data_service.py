from uuid import UUID

import crud_operations
from models import Department, DepartmentRole
from schemas import UserCreate
from validators import (format_and_validate_department_name,
                        format_and_validate_role)


def process_qr_data(db, uuid_code, username, role, department_name):
    validated_department = department_name.strip().capitalize()
    validated_role = role.strip().lower()

    user = None
    if uuid_code and UUID(uuid_code):
        user = crud_operations.get_user_by_id(db, uuid_code)

    if user:
        department = crud_operations.get_department_by_name(db, validated_department)
        if not department:
            department = Department(name=validated_department)
            db.add(department)
            db.flush()

        # Find the user's role for the specific department or create a new one if not found
        user_role = next(
            (
                role
                for role in user.department_roles
                if role.department_id == department.id
            ),
            None,
        )
        if user_role:
            if user_role.department.name != validated_department:
                user_role.department.name = validated_department
            if user_role.role != validated_role:
                user_role.role = validated_role
        else:
            # If the user doesn't have a role in the new department, create one
            new_department_role = DepartmentRole(
                user_id=user.id, department_id=department.id, role=validated_role
            )
            db.add(new_department_role)

        db.commit()

        return {
            "user_id": uuid_code,
            "username": username,
            "department_name": validated_department,
            "role": validated_role,
        }

    elif uuid_code == None:
        new_user = UserCreate(name=username)
        db_user = crud_operations.create_user(db, new_user)

        department = crud_operations.get_department_by_name(db, validated_department)
        if not department:
            department = Department(name=validated_department)
            db.add(department)
            db.flush()

        new_department_role = DepartmentRole(
            user_id=db_user.id, department_id=department.id, role=validated_role
        )
        db.add(new_department_role)
        db.commit()

        return {
            "user_id": db_user.id,
            "username": db_user.name,
            "department_name": validated_department,
            "role": validated_role,
        }

    else:
        return {
            "detail": "No user found with the provided UUID and no new user was created."
        }
