from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, LargeBinary, Float
from .base import BaseModel, Base

ADMIN = 1
AUTHER = 2
CUSTOMER = 3


class Users(Base, BaseModel):
    __tablename__ = 'users'

    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(Integer, nullable=False, default=1)
    address = Column(String, nullable=True)
    role = Column(String, nullable=True)
