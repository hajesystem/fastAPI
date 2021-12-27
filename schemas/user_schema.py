from pydantic import BaseModel
from typing import List

from schemas.info_schema import InfoOut
from schemas.todo_schema import TodoOut


class UserIn(BaseModel):
    user: str
    password: str


class UserOut(BaseModel):
    id: str
    user: str
    info: InfoOut
    todos: List[TodoOut]
    # class Config():       ─┬─> response_model을 사용하기 위하여 지정
    #   orm_mode = True     ─┘

    class Config():
        orm_mode = True


class UserInfoOut(BaseModel):
    id: str
    user: str
    info: InfoOut

    class Config():
        orm_mode = True
