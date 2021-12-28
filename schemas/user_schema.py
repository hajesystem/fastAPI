from pydantic import BaseModel
from typing import List, Optional

from schemas.info_schema import InfoOut
from schemas.todo_schema import TodoOut


class UserIn(BaseModel):
    user: str
    password: str


class UserOut(BaseModel):
    id: str
    user: str
    info: Optional[InfoOut]
    todos: Optional[List[TodoOut]]
    # class Config():       ─┬─> response_model을 사용하기 위하여 지정
    #   orm_mode = True     ─┘

    class Config():
        orm_mode = True


class UserToken(BaseModel):
    id: int
    user: str
    password: str
