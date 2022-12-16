from datetime import datetime

from pydantic import BaseModel


class GroupsBase(BaseModel):
    name: str


class GroupsCreate(GroupsBase):
    pass


class Groups(GroupsBase):
    id: int
    create_datetime: datetime | None

    class Config:
        orm_mode = True
