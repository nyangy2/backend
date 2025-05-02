from sqlalchemy import Column, Integer, String
from app.db.base import Base

class ChronicCondition(Base):
    __tablename__ = "chronic_conditions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)         # 한글명
    name_eng = Column(String, nullable=True)       # 영어명
    icd_code = Column(String, nullable=True)       # ICD-10 코드