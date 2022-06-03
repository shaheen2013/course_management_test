from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, LargeBinary, Float
from datetime import date


Base = declarative_base()


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Date, default=date.today())
    updated_at = Column(Date, default=date.today())
