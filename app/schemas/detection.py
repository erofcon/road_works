from datetime import datetime
from pydantic import BaseModel


class DetectionBase(BaseModel):
    descriptions: str | None
    creator_id: int | None


class DetectionCreate(DetectionBase):
    pass


class Detection(DetectionBase):
    id: int
    create_datetime: datetime

    class Config:
        orm_mode = True


class DetectionWithUserName(Detection):
    username: str
    detection_image_count: int


class DetectionWithLocations(BaseModel):
    id: int
    descriptions: str | None
    create_datetime: datetime | None
    creator_id: int
    locations: list | None
