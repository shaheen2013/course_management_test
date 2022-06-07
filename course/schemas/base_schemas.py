from pydantic import BaseModel
from datetime import datetime


class CreateBaseDataModel(BaseModel):
    created_at: datetime = datetime.now()


class UpdateBaseModelData(BaseModel):
    id: int
    updated_at: datetime = datetime.now()


class BaseModelData(CreateBaseDataModel, UpdateBaseModelData):
    pass


class PageData(BaseModel):
    page_size: int = 10
    page: int = 1
