from datetime import datetime

from pydantic import BaseModel


class JWTMeta(BaseModel):
    exp: datetime


class JWTUser(BaseModel):
    username: str
    sub: str
