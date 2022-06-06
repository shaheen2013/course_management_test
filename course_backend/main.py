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
from data_parsing import UpdateUserData, CreateUserData, CreateCourseData, \
    UpdateCourseData, CreateVideosData, UpdateVideosData, CreatePurchaseData, UpdatePurchaseData


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()


@app.post("/user/create")
async def create_user(user_data: CreateUserData):
    session = Session()
    session.add(Users(**user_data.dict()))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.get("/user/{id}")
async def find_user(id: int):
    session = Session()
    user = session.query(Users).filter(Users.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": jsonable_encoder({"user": user})
    })


@app.get("/users")
async def get_users(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    users = session.query(Users).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": jsonable_encoder({"users": users})
    })


@app.put("/user/update")
async def update_user(user: UpdateUserData):
    session = Session()
    session.add(session.merge(Users(**user.dict())))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.delete("/user/delete")
async def delete_user(id: int):
    session = Session()
    user = session.query(Users).get(id)
    session.delete(user)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.post("/course/create")
async def create_course(course: CreateCourseData):
    session = Session()
    course = course.dict()
    user = session.query(Users).filter(Users.id == course.get("user_id")).first()
    if user:
        if user.user_type != UserType.AUTHER:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "message": "User must be author!"
            })
        session.add(Courses(**course))
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content=get_success_msg())


@app.get("/course/{id}")
async def find_course(id: int):
    session = Session()
    course = session.query(Courses).filter(Courses.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": jsonable_encoder({"courses": course})
    })


@app.get("/courses")
async def get_courses(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    courses = session.query(Courses).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": jsonable_encoder({"courses": courses})
    })


@app.put("/course/update")
async def update_course(course: UpdateCourseData):
    session = Session()
    session.add(session.merge(Courses(**course.dict())))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.delete("/course/delete")
async def delete_course(id: int):
    session = Session()
    course = session.query(Courses).get(id)
    session.delete(course)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.post("/course/video/create")
async def create_video(video: CreateVideosData):
    session = Session()
    session.add(Videos(**video.dict()))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.put("/course/video/update")
async def update_video(video: UpdateVideosData):
    session = Session()
    session.add(session.merge(Videos(**video.dict())))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.delete("/course/video/delete")
async def delete_video(id: int):
    session = Session()
    video = session.query(Videos).get(id)
    session.delete(video)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@app.get("/course/video/{course_id}")
async def find_video_course_wise(course_id: int):
    session = Session()
    videos = session.query(Videos).filter(Videos.course_id == course_id)
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": jsonable_encoder({"videos": videos})
    })


@app.post("/purchase/create")
async def purchase_create(purchase: CreatePurchaseData):
    session = Session()
    purchase = purchase.dict()
    user = session.query(Users).filter(Users.id == purchase.get("user_id")).first()
    if user:
        if user.user_type != UserType.CUSTOMER:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "message": "User must be customer!"
            })
        session.add(Purchase(**purchase))
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content=get_success_msg())


def get_success_msg():
    return {
        "status_code": 200,
        "message": "success"
    }


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "message": message
    })
