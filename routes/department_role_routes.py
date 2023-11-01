from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud_operations
from main import get_db
from schemas import DepartmentRole

router = APIRouter()


@router.get("/department_roles/", response_model=List[DepartmentRole])
def read_department_roles(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
):
    """
    Get all department roles
    """
    roles = crud_operations.get_department_roles(db, skip=skip, limit=limit)
    if roles is None:
        raise HTTPException(status_code=404, detail="Department roles not found")
    return roles
