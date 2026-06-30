from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Role(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    VOLUNTEER = "volunteer"


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None
    role: Role


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(RegisterUser):
    user_id: Optional[UUID] = None
    email_verified: bool = False
    updated_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    deleted_by: Optional[UUID] = None
    deleted_at: Optional[datetime] = None


class UserId(BaseModel):
    user_id: UUID


class CreateUserWithConfirm(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserContext(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    role: Role
    email_verified: bool


class GetUserContext(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[EmailStr] = None


# jwt Payload
#
class UserPayload(UserContext):
    type: str


# token
#
class Token(BaseModel):
    access_token: str


# Email Verify


class EmailVerify(BaseModel):
    email: EmailStr
    email_verified: bool = False
