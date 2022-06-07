from .base_schemas import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel, EmailStr
from enum import Enum


class UserType(str, Enum):
    ADMIN = "Admin"
    AUTHER = "Author"
    CUSTOMER = "Customer"


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

