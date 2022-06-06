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
from data_parsing import UsersData


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()


@app.post("/user/create")
async def create_user(user_data: UsersData):
    session = Session()
    session.add(Users(**user_data.dict()))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.get("/user/{id}")
async def find_user(id: int):
    session = Session()
    user = session.query(Users).filter(Users.id == id).first()
    session.close()
    result = jsonable_encoder({"user": user})
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })


@app.get("/users")
async def get_users(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    users = session.query(Users).limit(page_size).offset(page * page_size).all()
    session.close()
    result = jsonable_encoder({
        "users": users
    })
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })


@app.put("/user/update")
async def update_user(id: int, name: str = None, email: str = None, address: str = None):
    session = Session()
    user = session.query(Users).get(id)
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if address is not None:
        user.address = address
    user.updated_at = date.today()
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.delete("/user/delete")
async def delete_user(id: int):
    session = Session()
    user = session.query(Users).get(id)
    session.delete(user)
    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.post("/course/create")
async def create_course(user_id: int, title: str, price: float, thumbnail_url: str):
    session = Session()
    user = session.query(Users).filter(Users.id == user_id).first()
    if user:
        if user.user_type != UserType.AUTHER:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "message": "User must be author!"
            })
        course = Courses(
            user_id=user_id,
            title=title,
            price=price,
            thumbnail_url=thumbnail_url
        )
        session.add(course)
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content={
            "status_code": 200,
            "message": "success"
        })


@app.get("/course/{id}")
async def find_course(id: int):
    session = Session()
    course = session.query(Courses).filter(Courses.id == id).first()
    session.close()
    result = jsonable_encoder({"courses": course})
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })


@app.get("/courses")
async def get_courses(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    courses = session.query(Courses).limit(page_size).offset(page * page_size).all()
    session.close()
    result = jsonable_encoder({
        "courses": courses
    })
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })


@app.put("/course/update")
async def update_course(id: int, title: str = None, price: float = None, thumbnail_url: str = None):
    session = Session()
    course = session.query(Courses).get(id)
    if title is not None:
        course.title = title
    if price is not None:
        course.price = price
    if thumbnail_url is not None:
        course.thumbnail_url = thumbnail_url
    course.updated_at = date.today()
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.delete("/course/delete")
async def delete_course(id: int):
    session = Session()
    course = session.query(Courses).get(id)
    session.delete(course)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.post("/course/video/create")
async def create_video(course_id: int, title: str, duration: int, description: str, video_url: str, thumbnail_url: str):
    session = Session()
    video = Videos(
        course_id=course_id,
        title=title,
        duration=duration,
        description=description,
        video_url=video_url,
        thumbnail_url=thumbnail_url
    )
    session.add(video)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.put("/course/video/update")
async def update_video(id: int, course_id: int = None, title: str = None, duration: int = None,
                       description: str = None, video_url: str = None, thumbnail_url: str = None):
    session = Session()
    video = session.query(Videos).get(id)
    if course_id is not None:
        video.course_id = course_id
    if title is not None:
        video.title = title
    if duration is not None:
        video.duration = duration
    if description is not None:
        video.description = description
    if video_url is not None:
        video.video_url = video_url
    if thumbnail_url is not None:
        video.thumbnail_url = thumbnail_url
    video.updated_at = date.today()
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.delete("/course/video/delete")
async def delete_video(id: int):
    session = Session()
    video = session.query(Videos).get(id)
    session.delete(video)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
    })


@app.get("/course/video/{course_id}")
async def find_video_course_wise(course_id: int):
    session = Session()
    videos = session.query(Videos).filter(Videos.course_id == course_id)
    session.close()
    result = jsonable_encoder({"videos": videos})
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })


@app.post("/purchase/create")
async def purchase_create(course_id: int, user_id: int, purchase_amount: float):
    session = Session()
    user = session.query(Users).filter(Users.id == user_id).first()
    if user:
        if user.user_type != UserType.CUSTOMER:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "message": "User must be customer!"
            })
        purchase = Purchase(
            course_id=course_id,
            user_id=user_id,
            purchase_amount=purchase_amount,
        )
        session.add(purchase)
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content={
            "status_code": 200,
            "message": "success"
        })


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "message": message
    })
