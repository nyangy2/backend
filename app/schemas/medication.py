from pydantic import BaseModel
from typing import Literal, Optional, List

class MedicationSearchRequest(BaseModel):
    product_name: str

class MedicationSearchRequest(BaseModel):
    product_name: str
    company: str

class MedicationDetailResponse(BaseModel):
    product_code: str
    product_name: str
    ingredient_name: str | None = None
    atc_name: str | None = None



# 요청: 새로 추가하려는 item_seq
class InteractionCheckRequest(BaseModel):
    new_medication_id: str  # item_seq of the medication to be checked

class InteractionItem(BaseModel):
    ingredient_a: str
    product_a: str
    manufacturer_a: Optional[str] = ""
    ingredient_b: str
    product_b: str
    manufacturer_b: Optional[str] = ""
    detail: str

class InteractionCheckResponse(BaseModel):
    interactions: List[InteractionItem]

class CondensedInteractionItem(BaseModel):
    product_a: str
    manufacturer_a: Optional[str] = ""
    interaction_type: str
    detail: str

class AlternativeDrug(BaseModel):
    item_name: str
    item_seq: str
    manufacturer: str
    ingredient: str

class CondensedInteractionResponse(BaseModel):
    interactions: List[CondensedInteractionItem]
    alternative_drugs: List[AlternativeDrug] = []