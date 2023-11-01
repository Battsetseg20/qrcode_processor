# validators.py
from uuid import UUID

from sqlalchemy.orm import Session

from models import Department, DepartmentRole, User

"""
This module contains functions that validate data and can be called from every other module.
"""


def is_user_admin_of_department(user: User, department_id: UUID) -> bool:
    """
    Check if a user has an admin role for a specific department.
    """
    for department_role in user.department_roles:
        if (
            department_role.department_id == department_id
            and department_role.role == "admin"
        ):
            return True
    return False


def format_and_validate_department_name(department_name: str) -> str:
    """
    Format and validate a department name.
    """
    VALID_DEPARTMENTS = ["Hr", "Engineering", "Marketing", "Finance", "Sales"]
    formatted_name = department_name.replace("_", " ").title()
    if formatted_name in VALID_DEPARTMENTS:
        return formatted_name
    raise ValueError(
        f"Wrong department! Please choose between {', '.join(VALID_DEPARTMENTS)}"
    )


def format_and_validate_role(role: str) -> str:
    """
    Format and validate a role.
    """
    VALID_ROLES = ["member", "admin"]
    if role in VALID_ROLES:
        return role
    raise ValueError(f"Invalid role! Please choose between {', '.join(VALID_ROLES)}")
