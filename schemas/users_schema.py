from pydantic import BaseModel
from typing import Optional


class UsersSchema(BaseModel):
    id: Optional[int]
    user: str
    name: str


class InfoSchema(BaseModel):
    id: Optional[int]
    email: str
    phone: str
    address: str
