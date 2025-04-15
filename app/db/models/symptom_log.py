from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class SymptomSearchLog(Base):
    __tablename__ = "symptom_search_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    symptom = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
