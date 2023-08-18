from pydantic import BaseModel


class UsersGroupsBase(BaseModel):
    user_id: int
    group_id: int


class UsersGroupsBaseCreate(UsersGroupsBase):
    pass


class UsersGroups(UsersGroupsBase):
    id: int

    class Config:
        orm_mode = True
