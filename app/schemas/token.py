from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    username: str | None


class TokenUser(BaseModel):
    username: str
