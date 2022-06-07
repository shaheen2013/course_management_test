from .base_schemas import UpdateBaseModelData, CreateBaseDataModel
from pydantic import BaseModel, FilePath


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
    video_url: FilePath
    thumbnail_url: FilePath
    duration: int
    free_preview: bool = False


class CreateVideos(VideosData, CreateBaseDataModel):
    course_id: int


class UpdateVideos(VideosData, UpdateBaseModelData):
    pass


class PurchaseData(BaseModel):
    course_id: int
    user_id: int
    purchase_amount: float


class CreatePurchase(PurchaseData, CreateBaseDataModel):
    pass


class UpdatePurchase(PurchaseData, UpdateBaseModelData):
    pass
