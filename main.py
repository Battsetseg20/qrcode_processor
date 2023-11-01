import json
import os
from typing import List
from uuid import UUID

# Local Imports
import crud_operations
import models
import schemas as schema
from database import Base, SessionLocal, engine, get_db
# Third-party Imports
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes import (department_role_routes, department_routes, qrcode_routes,
                    user_routes)
from security import authenticate_user, create_access_token
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from validators import (format_and_validate_department_name,
                        format_and_validate_role, is_user_admin_of_department)

"""
Entry point of the application.
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Creating the tables")
try:
    Base.metadata.create_all(bind=engine)
except OperationalError as e:
    print("Unable to access postgresql database:", e)


"""
Routes
"""


@app.get("/", response_model=dict, tags=["Root route"])
def read_root():
    return {"message": "Hello, world!"}


@app.post("/token", response_model=dict, tags=["Authentication token"])
def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(qrcode_routes.router, tags=["Upload Qrcodes files"])
app.include_router(user_routes.router, tags=["Users"])
app.include_router(department_routes.router, tags=["Departments"])
app.include_router(department_role_routes.router, tags=["Department roles"])
