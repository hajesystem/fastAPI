from datetime import date
from pydantic import BaseModel


class TodoIn(BaseModel):
    date: date
    titile: str
    descript: str
    user_id: int


class TodoOut(BaseModel):
    id: int
    date: date
    titile: str
    descript: str
    # user_id: int

    class Config():
        orm_mode = True
