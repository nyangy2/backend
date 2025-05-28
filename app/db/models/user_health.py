from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DateTime, func,  Boolean
from app.db.base import Base

class UserDrug(Base):
    __tablename__ = "user_drugs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_seq = Column(String, ForeignKey("medications.item_seq", ondelete="CASCADE"), nullable=False)
    item_name = Column(String, nullable=False)
    entp_name = Column(String)
    atc_code = Column(String)
    main_ingr_eng = Column(String)
    main_item_ingr = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    morning = Column(Boolean, nullable=False, default=False)
    afternoon = Column(Boolean, nullable=False, default=False)
    evening = Column(Boolean, nullable=False, default=False)
    
class UserCondition(Base):
    __tablename__ = "user_conditions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    condition_id = Column(Integer, ForeignKey("chronic_conditions.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)       # 질환 한글명 복사
    name_eng = Column(String, nullable=True)    # 영어명
    icd_code = Column(String, nullable=True)    # ICD 코드

    created_at = Column(DateTime(timezone=True), server_default=func.now())

