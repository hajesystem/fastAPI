from pydantic import BaseModel
from typing import Optional


class UserIn(BaseModel):
    user: str
    password: str


class UserOut(BaseModel):
    id: str
    user: str
    # class Config():       ─┬─> response_model을 사용하기 위하여 지정
    #   orm_mode = True     ─┘

    class Config():
        orm_mode = True


class UserInfoIn(BaseModel):
    name: str
    email: str
    phone: str
