from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, LargeBinary, Float
from .base import BaseModel, Base


class Courses(Base, BaseModel):
    __tablename__ = 'courses'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String)
    price = Column(Float)
    thumbnail_url = Column(String, nullable=True)


class Videos(Base, BaseModel):
    __tablename__ = 'videos'

    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String)
    description = Column(String, nullable=True)
    video_url = Column(String)
    thumbnail_url = Column(String, nullable=True)
    duration = Column(Integer)
    free_preview = Column(Boolean, default=False)


class Purchase(Base, BaseModel):
    __tablename__ = 'purchases'

    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    purchase_amount = Column(Float)

