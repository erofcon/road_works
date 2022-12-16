from datetime import datetime

from pydantic import BaseModel


class CompaniesBase(BaseModel):
    name: str
    is_creator: bool


class CompaniesCreate(CompaniesBase):
    pass


class Companies(CompaniesBase):
    id: int
    create_datetime: datetime

    class Config:
        orm_mode = True
