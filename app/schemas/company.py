from datetime import datetime

from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    is_creator: bool


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    create_datetime: datetime

    class Config:
        orm_mode = True
