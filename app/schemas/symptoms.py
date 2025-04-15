from typing import List
from pydantic import BaseModel



class SymptomSearchRequest(BaseModel):
    keywords: List[str]

class DrugRecommendation(BaseModel):
    drug_id: int
    drug_name: str
    score: float