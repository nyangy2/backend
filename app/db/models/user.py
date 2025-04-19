from sqlalchemy import Column, String, Integer
from app.db.base import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    drugs = relationship("UserDrug", back_populates="user", cascade="all, delete")
    health_info = relationship("UserHealthInfo", back_populates="user", cascade="all, delete")
    
