from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import date
from config.settings import DATABASE_URL
from models.course import Courses, Videos, Purchase
from models.users import Users, UserType
from models.base import Base
from schemas import UpdateUserData, CreateUserData, CreateCourseData, \
    UpdateCourseData, CreateVideosData, UpdateVideosData, CreatePurchaseData, UpdatePurchaseData
from utils import *


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()


@app.post("/user/create")
async def create_user(user_data: CreateUserData):
    add_model_data(Users, user_data)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.get("/user/{id}")
async def find_user(id: int):
    session = Session()
    user = session.query(Users).filter(Users.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"user": user})))


@app.get("/users")
async def get_users(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    users = session.query(Users).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"users": users})))


@app.put("/user/update")
async def update_user(user: UpdateUserData):
    update_model_data(Users, user)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.delete("/user/delete")
async def delete_user(id: int):
    delete_model_data(Users, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.post("/course/create")
async def create_course(course: CreateCourseData):
    session = Session()
    course = course.dict()
    user = session.query(Users).filter(Users.id == course.get("user_id")).first()
    if user:
        if user.user_type != UserType.AUTHER:
            return JSONResponse(status_code=200, content=get_invalid_msg("User must be author!"))
        session.add(Courses(**course))
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content=get_success_msg())


@app.get("/course/{id}")
async def find_course(id: int):
    session = Session()
    course = session.query(Courses).filter(Courses.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"courses": course})))


@app.get("/courses")
async def get_courses(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    courses = session.query(Courses).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"courses": courses})))


@app.put("/course/update")
async def update_course(course: UpdateCourseData):
    update_model_data(Courses, course)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.delete("/course/delete")
async def delete_course(id: int):
    delete_model_data(Courses, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.post("/course/video/create")
async def create_video(video: CreateVideosData):
    add_model_data(Videos, video)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.put("/course/video/update")
async def update_video(video: UpdateVideosData):
    update_model_data(Videos, video)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.delete("/course/video/delete")
async def delete_video(id: int):
    delete_model_data(Videos, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@app.get("/course/video/{course_id}")
async def find_video_course_wise(course_id: int):
    session = Session()
    videos = session.query(Videos).filter(Videos.course_id == course_id)
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"videos": videos})))


@app.post("/purchase/create")
async def purchase_create(purchase: CreatePurchaseData):
    session = Session()
    purchase = purchase.dict()
    user = session.query(Users).filter(Users.id == purchase.get("user_id")).first()
    if user:
        if user.user_type != UserType.CUSTOMER:
            return JSONResponse(status_code=200, content=get_invalid_msg("User must be customer!"))
        session.add(Purchase(**purchase))
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content=get_success_msg())


def delete_model_data(model, id):
    session = Session()
    obj = session.query(model).get(id)
    session.delete(obj)
    session.commit()
    session.close()


def add_model_data(model, data):
    session = Session()
    session.add(model(**data.dict()))
    session.commit()
    session.close()


def update_model_data(model, data):
    session = Session()
    session.add(session.merge(model(**data.dict())))
    session.commit()
    session.close()


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "message": message
    })
