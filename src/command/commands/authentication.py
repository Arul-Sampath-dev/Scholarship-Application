from datetime import datetime
from enum import Enum
from optparse import Option
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
    is_active: bool = True
    email_verified: bool = False
    account_verified: bool = False
    verified_by: Optional[UUID] = None
    updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None


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
    account_verified: bool


class GetUserContext(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[EmailStr] = None


# Provider Table


class Provider(Enum):
    GOOGLE = "google"
    MICROSOFT = "microsoft"


class ProviderCreate(BaseModel):
    provider_name: Provider
    user_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)


class ProviderGet(BaseModel):
    provider_name: Provider
    user_id: UUID
    created_at: datetime
    provider_id: UUID


class UserHasProvider(BaseModel):
    user_id: UUID
    provider_name: Provider


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
