from pydantic import BaseModel


class InfoIn(BaseModel):
    name: str
    email: str
    phone: str
    user_id: int


class InfoOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    user_id: int

    class Config():
        orm_mode = True
