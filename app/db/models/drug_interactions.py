from sqlalchemy import Column, Integer, Text
from app.db.base import Base


class DrugInteraction(Base):
    __tablename__ = "drug_interactions"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_a = Column(Text)
    product_a = Column(Text)
    manufacturer_a = Column(Text)
    ingredient_b = Column(Text)
    product_b = Column(Text)
    manufacturer_b = Column(Text)
    detail = Column(Text)
