from datetime import datetime

from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    create_datetime: datetime | None

    class Config:
        orm_mode = True
