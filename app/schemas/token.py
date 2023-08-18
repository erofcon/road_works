from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    id: int | None
    username: str | None


class TokenUser(BaseModel):
    username: str


class TokenQuery(BaseModel):
    access_token: str
    refresh_token: str
    user: dict | None


class TokenData(BaseModel):
    sub: str
    user: dict | None
