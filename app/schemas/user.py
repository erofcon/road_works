from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str | None
    surname: str | None
    phone_number: int | None
    email: str | None
    is_admin: bool | None
    related_company: int | None


class CreateUser(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# class User(BaseModel):
#     id: int
#     username: str


class UserWithCheckCreatorStatus(BaseModel):
    """

    """
    id: int
    username: str
    name: str | None
    phone_number: int | None
    email: str | None
    is_admin: bool | None
    is_creator: bool | None

    class Config:
        orm_mode = True


class UserWithCheckCreatorStatusAndPassword(UserWithCheckCreatorStatus):
    """

    """
    password: str | None
