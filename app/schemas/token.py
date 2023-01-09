from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    id: int | None
    username: str | None


class TokenUser(BaseModel):
    username: str
