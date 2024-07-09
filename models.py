# models.py
from sqlalchemy import Column, Integer, TIMESTAMP, Boolean, String, LargeBinary, Text
from database import Base

class Fabric(Base):
    __tablename__ = "production_history"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(TIMESTAMP(), index=True)
    status = Column(Boolean(),  index=True)
    file = Column(String(100), index=True)

class FabricImage(Base):
    __tablename__ = "production_images"

    id = Column(Integer, primary_key=True, index=True)
    input_image = Column(Text(length=16777215))  # MEDIUMTEXT
    output_image = Column(Text(length=16777215))  # MEDIUMTEXT
    history_id = Column(Integer, index=True, unique=True)


