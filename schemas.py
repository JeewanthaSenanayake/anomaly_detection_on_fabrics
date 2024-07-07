# schemas.py
from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Boolean

class FabricBase(BaseModel):
    date: TIMESTAMP
    status: Boolean

class Fabric(FabricBase):
    id: int

    class Config:
        orm_mode = True
