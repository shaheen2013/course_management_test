from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from course.config.database import Session
from course.models.course import Purchase
from course.models.users import Users, UserType
from course.schemas import CreatePurchase
from course.utils import *


router = APIRouter(
    prefix="/purchase",
    tags=['Purchases']
)


@router.post("/create")
async def purchase_create(request: CreatePurchase):
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
