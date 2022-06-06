from .base_parsing import BaseDataModel
# from ..models import UserType
from enum import Enum


class UserType(str, Enum):
    ADMIN = "Admin"
    AUTHER = "Author"
    CUSTOMER = "Customer"


class UsersData(BaseDataModel):
    name: str
    email: str
    hashed_password: str
    is_active: bool = True
    user_type: UserType
    address = str
