from fastapi import APIRouter
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from course_backend.config.database import Session, add_model_data, update_model_data,\
    delete_model_data
from course_backend.models.course import Courses, Videos, Purchase
from course_backend.models.users import Users, UserType
from course_backend.schemas import CreateCourse, \
    UpdateCourse, CreateVideos, UpdateVideosData
from course_backend.utils import *
from fastapi import File, UploadFile
import shutil


router = APIRouter(
    prefix="/course",
    tags=['Courses']
)


@router.post("/create")
async def create_course(request: CreateCourse):
    session = Session()
    course = request.dict()
    user = session.query(Users).filter(Users.id == course.get("user_id")).first()
    if user:
        if user.user_type != UserType.AUTHER:
            return JSONResponse(status_code=200, content=get_invalid_msg("User must be author!"))
        session.add(Courses(**course))
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content=get_success_msg())


@router.get("/{id}")
async def find_course(id: int):
    session = Session()
    course = session.query(Courses).filter(Courses.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"courses": course})))


@router.get("/list")
async def get_courses(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    courses = session.query(Courses).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"courses": courses})))


@router.put("/update")
async def update_course(course: UpdateCourse):
    update_model_data(Courses, course)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.delete("/delete")
async def delete_course(id: int):
    delete_model_data(Courses, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.post("/video/create")
async def create_video(request: CreateVideos):
    add_model_data(Videos, request.dict())
    return JSONResponse(status_code=200, content=get_success_msg())


@router.put("/video/update")
async def update_video(request: UpdateVideosData):
    update_model_data(Videos, request)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.delete("/video/delete")
async def delete_video(id: int):
    delete_model_data(Videos, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.get("/video/{course_id}")
async def find_video_course_wise(course_id: int):
    session = Session()
    videos = session.query(Videos).filter(Videos.course_id == course_id)
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"videos": videos})))