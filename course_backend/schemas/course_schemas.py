from .base_schemas import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel


class CourseData(BaseModel):
    title: str
    price: float
    thumbnail_url: str


class CreateCourse(CourseData, CreateBaseDataModel):
    user_id: int


class UpdateCourse(CourseData, UpdateBaseModelData):
    pass


class VideosData(BaseModel):
    title: str
    description: str
    video_url: str
    thumbnail_url: str
    duration: int
    free_preview: bool = False


class CreateVideos(VideosData, CreateBaseDataModel):
    course_id: int


class UpdateVideosData(VideosData, UpdateBaseModelData):
    pass


class PurchaseData(BaseModel):
    course_id: int
    user_id: int
    purchase_amount: float


class CreatePurchase(PurchaseData, CreateBaseDataModel):
    pass


class UpdatePurchase(PurchaseData, UpdateBaseModelData):
    pass