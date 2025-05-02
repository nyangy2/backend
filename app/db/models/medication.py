from sqlalchemy import Column, String, Text
from app.db.base import Base

class Medication(Base):
    __tablename__ = "medications"

    item_seq = Column(String, primary_key=True)
    item_name = Column(Text, nullable=False)
    entp_name = Column(Text)
    etc_otc_code = Column(Text)
    main_item_ingr = Column(Text)
    main_ingr_eng = Column(Text)
    atc_code = Column(Text)
