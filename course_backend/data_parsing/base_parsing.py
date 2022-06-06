from pydantic import BaseModel
from datetime import datetime, date


class CreateBaseDataModel(BaseModel):
    created_at: date
    updated_at: date = date.today()


class UpdateBaseModelData(BaseModel):
    id: int


class BaseModelData(CreateBaseDataModel, UpdateBaseModelData):
    pass
