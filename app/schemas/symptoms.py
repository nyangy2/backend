from typing import List
from pydantic import BaseModel



class SymptomSearchRequest(BaseModel):
    symptoms: List[str]

class DrugRecommendation(BaseModel):
    drug_id: int
    drug_name: str
    entp_name: str


class SymptomSearchResult(BaseModel):
    id: int
    name: str
    name_eng: str