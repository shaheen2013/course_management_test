from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from course.models.users import Users
from course.schemas import UpdateUser, CreateUser, TokenUser, PageData
from course.utils import *
from course.utils.hashing import Hash
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from course.authentication import oauth2
from course.config.database import Session, add_model_data, update_model_data,\
    delete_model_data


router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.post("/create")
async def create_user(request: CreateUser):
    user_data = request.dict()
    user_data.update({"hashed_password": Hash.bcrypt(user_data.get("hashed_password"))})
    add_model_data(Users, user_data)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.get("/{id}")
async def find_user(id: int, current_user: TokenUser = Depends(oauth2.get_current_user)):
    session = Session()
    user = session.query(Users).filter(Users.id == id).first()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"user": user})))


@router.post("/list")
async def get_users(page: PageData, current_user: TokenUser = Depends(oauth2.get_current_user)):
    data = page.dict()
    page = data.get("page")
    page_size = data.get("page_size")
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    users = session.query(Users).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"users": users})))


@router.put("/update")
async def update_user(request: UpdateUser, current_user: TokenUser = Depends(oauth2.get_current_user)):
    update_model_data(Users, request)
    return JSONResponse(status_code=200, content=get_success_msg())


@router.delete("/delete")
async def delete_user(id: int, current_user: TokenUser = Depends(oauth2.get_current_user)):
    delete_model_data(Users, id)
    return JSONResponse(status_code=200, content=get_success_msg())

