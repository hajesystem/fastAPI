from pydantic import BaseModel
from typing import Optional


class BasicSchema(BaseModel):
    id: Optional[int]
    title: str
    descript: str
    option: Optional[str]  # 옵션으로 값이 없어도 된다.
