# app\schemas\user.py

from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
import pytz
from enum import Enum

tz = pytz.timezone('Asia/Bangkok')

class RoleEnum(int, Enum):
    admin = 1
    user = 2
    editor = 3

    @classmethod
    def to_string(cls, role: int) -> Optional[str]:
        """Map integer to the string role."""
        if role == cls.admin:
            return "admin"
        elif role == cls.user:
            return "user"
        elif role == cls.editor:
            return "editor"
        return None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: constr(min_length=6) # type: ignore

class UserCreateAdmin(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=6) # type: ignore
    role: int  

    class Config:
        from_attributes = True
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional [EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

class UserAuth(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    # email: str
    old_password: str
    new_password: str

class ResetPasswordRequest(BaseModel):
    email: str

class UserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


