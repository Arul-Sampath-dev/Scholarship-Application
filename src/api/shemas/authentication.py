from pydantic import BaseModel, EmailStr

from src.command.commands.provider import Provider


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class FromProvider(BaseModel):
    username: str
    email: EmailStr
    provider: Provider


class LoginSuccess(BaseModel):
    message: str
