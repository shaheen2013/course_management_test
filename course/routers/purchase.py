from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from course.config.database import Session
from course.models.course import Purchase
from course.models.users import Users, UserType
from course.schemas import CreatePurchase, TokenUser, PageData
from course.authentication import oauth2
from course.utils import *
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/purchase",
    tags=['Purchases']
)


@router.post("/create")
async def purchase_create(request: CreatePurchase, current_user: TokenUser = Depends(oauth2.get_current_user)):
    session = Session()
    purchase = request.dict()
    user = session.query(Users).filter(Users.id == purchase.get("user_id")).first()
    if user:
        if user.user_type != UserType.CUSTOMER:
            return JSONResponse(status_code=200, content=get_invalid_msg("User must be customer!"))
        session.add(Purchase(**purchase))
        session.commit()
        session.close()
        return JSONResponse(status_code=200, content=get_success_msg())


@router.post("/list")
async def get_purchases(page: PageData, current_user: TokenUser = Depends(oauth2.get_current_user)):
    data = page.dict()
    page = data.get("page")
    page_size = data.get("page_size")
    if (page_size > 100 or page_size < 0):
        page_size = 100
    page -= 1
    session = Session()
    purchases = session.query(Purchase).limit(page_size).offset(page * page_size).all()
    session.close()
    return JSONResponse(status_code=200, content=get_response_data(jsonable_encoder({"purchases": purchases})))