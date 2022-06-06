from pydantic import BaseModel
from datetime import datetime, date


class BaseDataModel(BaseModel):
    # id: int
    created_at: date
    updated_at: date = date.today()
