from pydantic import BaseModel


class ValidationModel(BaseModel):
    table: str
    column: str
    item: str
