from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from course_backend.models.users import Users
from course_backend.schemas import UpdateUser, CreateUser
from course_backend.utils import *
from course_backend.utils.hashing import Hash
from fastapi import APIRouter
from sqlalchemy.orm import Session
from course_backend.config.database import Session, add_model_data, update_model_data,\
    delete_model_data


router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/create")
async def create_user(user_data: CreateUser):
    user_data = user_data.dict()
    user_data.update({"hashed_password": Hash.bcrypt(user_data.get("hashed_password"))})
    add_model_data(Users, user_data)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.get("/{id}")
async def find_user(id: int):
    session = Session()
    user = session.query(Users).filter(Users.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"user": user})))


@router.get("/list")
async def get_users(page_size: int = 10, page: int = 1):
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    users = session.query(Users).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"users": users})))


@router.put("/update")
async def update_user(user: UpdateUser):
    update_model_data(Users, user)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.delete("/delete")
async def delete_user(id: int):
    delete_model_data(Users, id)
    return JSONResponse(status_code=200, content=get_success_msg())

