from .base_schemas import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel


class CourseData(BaseModel):
    title: str
    price: float
    thumbnail_url: str


class CreateCourseData(CourseData, CreateBaseDataModel):
    user_id: int


class UpdateCourseData(CourseData, UpdateBaseModelData):
    pass


class VideosData(BaseModel):
    title: str
    description: str
    video_url: str
    thumbnail_url: str
    duration: int
    free_preview: bool = False


class CreateVideosData(VideosData, CreateBaseDataModel):
    course_id: int


class UpdateVideosData(VideosData, UpdateBaseModelData):
    pass


class PurchaseData(BaseModel):
    course_id: int
    user_id: int
    purchase_amount: float


class CreatePurchaseData(PurchaseData, CreateBaseDataModel):
    pass


class UpdatePurchaseData(PurchaseData, UpdateBaseModelData):
    pass
