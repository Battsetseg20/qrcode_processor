from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud_operations
from main import get_db
from schemas import Department
from security import get_current_user, verify_token
from validators import is_user_admin_of_department

router = APIRouter()


@router.delete("/department/{department_id}")
async def delete_department(
    department_id: UUID,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a department. Only admins of the department can delete it.
    """
    username = current_user
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = crud_operations.get_user_by_username(db, username)

    department = crud_operations.get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # if user is admin of department, delete department
    if not is_user_admin_of_department(user, department_id):
        raise HTTPException(
            status_code=403,
            detail="User does not have an admin permission for this department",
        )

    # Manually delete all roles associated with this department
    department_roles = crud_operations.get_department_roles_by_department_id(
        db, department_id
    )
    for role in department_roles:
        db.delete(role)
    try:
        # After deleting roles, delete the department
        db.delete(department)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting department: {e}")
    db.close()
    return {"message": "Department deleted successfully"}


@router.get("/departments/", response_model=List[Department])
def read_departments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get all departments
    """
    departments = crud_operations.get_departments(db, skip=skip, limit=limit)
    if departments is None:
        raise HTTPException(status_code=404, detail="Departments not found")
    return departments


@router.get("/department/{department_id}", response_model=Department)
def read_department(department_id: UUID, db: Session = Depends(get_db)):
    """
    Get a department by ID
    """
    department = crud_operations.get_department_by_id(db, department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department
