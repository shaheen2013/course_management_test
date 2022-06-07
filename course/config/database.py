from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import DATABASE_URL
from course.models.base import Base

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False,)
# Base = declarative_base()


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def delete_model_data(model, id):
    session = Session()
    obj = session.query(model).get(id)
    session.delete(obj)
    session.commit()
    session.close()


def add_model_data(model, data):
    session = Session()
    session.add(model(**data))
    session.commit()
    session.close()


def update_model_data(model, data):
    session = Session()
    session.add(session.merge(model(**data.dict())))
    session.commit()
    session.close()