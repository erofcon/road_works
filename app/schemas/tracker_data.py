from datetime import datetime

from pydantic import BaseModel


class TrackerDataBase(BaseModel):
    latitude: float
    longitude: float
    create_datetime: datetime
    car_id: int


class TrackerDataCreate(TrackerDataBase):
    pass


class TrackerData(TrackerDataBase):
    id: int

    class Config:
        orm_mode = True
       