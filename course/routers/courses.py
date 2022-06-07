from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from course.config.database import Session, add_model_data, update_model_data,\
    delete_model_data
from course.models.course import Courses, Videos, Purchase
from course.config.settings import BASE_DIR, DOMAIN_NAME
from course.models.users import Users, UserType
from course.schemas import CreateCourse, \
    UpdateCourse, TokenUser
from course.utils import *
from course.authentication import oauth2
from fastapi import File, UploadFile
import shutil


router = APIRouter(
    prefix="/course",
    tags=['Courses']
)


@router.post("/create")
async def create_course(request: CreateCourse, current_user: TokenUser = Depends(oauth2.get_current_user)):
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
async def find_course(id: int, current_user: TokenUser = Depends(oauth2.get_current_user)):
    session = Session()
    course = session.query(Courses).filter(Courses.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"courses": course})))


@router.post("/list")
async def get_courses(page_size: int = 10, page: int = 1, current_user: TokenUser = Depends(oauth2.get_current_user)):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    courses = session.query(Courses).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"courses": courses})))


@router.put("/update")
async def update_course(course: UpdateCourse, current_user: TokenUser = Depends(oauth2.get_current_user)):
    update_model_data(Courses, course)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.delete("/delete")
async def delete_course(id: int, current_user: TokenUser = Depends(oauth2.get_current_user)):
    delete_model_data(Courses, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.put("/video/upload/")
async def video_upload(course_id: int, title: str, description: str, duration: int, free_preview: bool = False,
                       thumbnail_url: UploadFile = File(None), video_url: UploadFile = File(None),
                       current_user: TokenUser = Depends(oauth2.get_current_user)):
    video_obj_data = {
       'course_id': course_id,
       "title": title,
       "description": description,
       "duration": duration,
       "free_preview": free_preview,
       "video_url": upload_file(video_url),
       "thumbnail_url": upload_file(thumbnail_url)
    }
    video_obj = Videos(**video_obj_data)
    session = Session()
    session.add(video_obj)
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


def upload_file(file_obj):
    try:
        with open(f'./media/{file_obj.filename}', 'wb') as buffer:
            shutil.copyfileobj(file_obj.file, buffer)
        return DOMAIN_NAME + str('/media/{0}').format(file_obj.filename)
    except Exception as e:
        return ""


@router.put("/video/update")
async def update_video(id: int, course_id: int, title: str, description: str, duration: int, free_preview: bool = False,
                       thumbnail_url: UploadFile = File(None), video_url: UploadFile = File(None),
                       current_user: TokenUser = Depends(oauth2.get_current_user)):
    video_obj_data = {
       'id': id,
       'course_id': course_id,
       "title": title,
       "description": description,
       "duration": duration,
       "free_preview": free_preview,
       "video_url": upload_file(video_url),
       "thumbnail_url": upload_file(thumbnail_url)
    }
    session = Session()
    session.add(session.merge(Videos(**video_obj_data)))
    session.commit()
    session.close()
    return JSONResponse(status_code=200, content=get_success_msg())


@router.delete("/video/delete")
async def delete_video(id: int, current_user: TokenUser = Depends(oauth2.get_current_user)):
    delete_model_data(Videos, id)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.get("/video/{course_id}")
async def find_video_course_wise(course_id: int, current_user: TokenUser = Depends(oauth2.get_current_user)):
    session = Session()
    videos = session.query(Videos).filter(Videos.course_id == course_id)
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"videos": videos})))