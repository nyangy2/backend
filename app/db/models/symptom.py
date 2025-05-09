from sqlalchemy import Column, Integer, String
from app.db.base import Base  # 당신의 프로젝트에 맞는 Base 경로

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    name_eng = Column(String, nullable=False)
    icd10_code = Column(String, unique=True, nullable=False)