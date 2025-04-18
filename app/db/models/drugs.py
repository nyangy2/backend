from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Drug(Base):
    __tablename__ = "drug"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
