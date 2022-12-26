from pydantic import BaseModel


class UsersBase(BaseModel):
    id: int
    username: str
    name: str | None
    surname: str | None
    phone_number: int | None
    email: str | None
    is_super_user: bool | None
    is_admin: bool | None
    related_company: int | None


class CreateUser(UsersBase):
    password: str


class Users(UsersBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    username: str
