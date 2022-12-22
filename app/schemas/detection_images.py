from pydantic import BaseModel


class DetectionImagesBase(BaseModel):
    url: str
    latitude: float
    longitude: float


class DetectionImagesCreate(DetectionImagesBase):
    pass


class DetectionImages(DetectionImagesBase):
    id: int
    detection_id: int

    class Config:
        orm_mode = True
