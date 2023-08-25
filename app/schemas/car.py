from datetime import datetime

from pydantic import BaseModel


class CarBase(BaseModel):
    imei: str
    car_number: str


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int
    create_datetime: datetime

    class Config:
        orm_mode = True
