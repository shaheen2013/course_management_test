from .base_parsing import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel


class CourseData(BaseModel):
    title: str
    price: float
    thumbnail_url: str


class CreateCourseData(CourseData, CreateBaseDataModel):
    user_id: int


class UpdateCourseData(CourseData, UpdateBaseModelData):
    pass

