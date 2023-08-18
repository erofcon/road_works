from pydantic import BaseModel


class DetectionLocationsBase(BaseModel):
    latitude: float
    longitude: float


class DetectionLocationsCreate(DetectionLocationsBase):
    pass


class DetectionLocation(DetectionLocationsBase):
    id: int
    detection_id: int
