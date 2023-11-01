from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

"""
Schemas classes use pydantic's BaseModel class to validate the structure of the data sent to and from the API.
"""


class QRCodeData(BaseModel):
    user_id: str
    department_id: str
    role: str


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attrinutes = True


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attrinutes = True


class DepartmentRoleBase(BaseModel):
    role: str


class DepartmentRoleCreate(DepartmentRoleBase):
    pass


class DepartmentRole(DepartmentRoleBase):
    user_id: UUID
    department_id: UUID
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attrinutes = True
