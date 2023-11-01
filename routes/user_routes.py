# /routes/user_routes.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud_operations
from main import get_db
from schemas import User

router = APIRouter()


@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get all users
    """
    users = crud_operations.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/user/{user_id}", response_model=User)
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Get a user by ID
    """
    user = crud_operations.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
