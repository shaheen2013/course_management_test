from .base_schemas import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional
from course.models import UserType


class UserData(BaseModel):
    name: str
    email: EmailStr
    address = str
    is_active: bool = True


class CreateUser(UserData, CreateBaseDataModel):
    hashed_password: str
    user_type: UserType


class UpdateUser(UserData, UpdateBaseModelData):
    pass


class TokenUser(BaseModel):
    name: str
    email: str
    password: str


class TokenData(BaseModel):
    email: Optional[str] = None
