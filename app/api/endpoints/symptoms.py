from fastapi import APIRouter, Query
from typing import List
from app.schemas.symptoms import SymptomSearchRequest, DrugRecommendation

router = APIRouter()

@router.get("/symptoms/popular", tags=["symptoms"])
async def get_popular_symptoms():
    return {
        "result": ["두통", "발열", "기침", "콧물", "복통"]
    }

@router.post("/symptoms/search", response_model=List[DrugRecommendation], tags=["symptoms"])
async def search_symptoms(req: SymptomSearchRequest):
    return [
        DrugRecommendation(drug_id=1, drug_name="타이레놀", score=0.95),
        DrugRecommendation(drug_id=2, drug_name="콜대원", score=0.87)
    ]

@router.get("/symptoms/by-body-part", tags=["symptoms"])
async def get_symptoms_by_body_part(part: str = Query(..., example="머리")):
    return {
        "result": ["두통", "눈 통증", "어지러움"]
    }
