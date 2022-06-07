from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, LargeBinary, Float
from .base import BaseModel, Base
from enum import Enum


class UserType(str, Enum):
    ADMIN = "Admin"
    AUTHER = "Author"
    CUSTOMER = "Customer"


class Users(Base, BaseModel):
    __tablename__ = 'users'

    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(String, nullable=False)
    address = Column(String, nullable=True)
