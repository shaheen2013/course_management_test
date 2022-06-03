from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, LargeBinary, Float
from datetime import date


ADMIN = 1
AUTHER = 2
CUSTOMER = 3

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(Integer, nullable=False, default=1)
    address = Column(String, nullable=True)
    created_at = Column(Date, default=date.today())
    updated_at = Column(Date, default=date.today())


class Courses(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String)
    price = Column(Float)
    thumbnail_url = Column(String, nullable=True)
    created_at = Column(Date, default=date.today())
    updated_at = Column(Date, default=date.today())


class Videos(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String)
    description = Column(String, nullable=True)
    video_url = Column(String)
    thumbnail_url = Column(String, nullable=True)
    duration = Column(Integer)
    free_preview = Column(Boolean, default=False)
    created_at = Column(Date, default=date.today())
    updated_at = Column(Date, default=date.today())


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    purchase_amount = Column(Float)
    created_at = Column(Date, default=date.today())
    updated_at = Column(Date, default=date.today())

