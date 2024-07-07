# models.py
from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, String
from database import Base

class Fabric(Base):
    __tablename__ = "production_history"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP(), index=True)
    status = Column(Boolean(),  index=True)
    file = Column(String(100), index=True)

