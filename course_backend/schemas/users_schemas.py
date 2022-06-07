from .base_schemas import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel
from enum import Enum


class UserType(str, Enum):
    ADMIN = "Admin"
    AUTHER = "Author"
    CUSTOMER = "Customer"


class UserData(BaseModel):
    name: str
    email: str
    address = str
    is_active: bool = True


class CreateUserData(UserData, CreateBaseDataModel):
    hashed_password: str
    user_type: UserType


class UpdateUserData(UserData, UpdateBaseModelData):
    pass

