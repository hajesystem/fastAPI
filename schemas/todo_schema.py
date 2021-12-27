from pydantic import BaseModel


class TodoIn(BaseModel):
    date: str
    title: str
    descript: str
    user_id: int


class TodoOut(BaseModel):
    id: int
    date: str
    title: str
    descript: str
    user_id: int

    class Config():
        orm_mode = True
