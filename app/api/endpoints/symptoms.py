from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# 응답 모델 예시
class DrugRecommendation(BaseModel):
    drug_id: int
    drug_name: str
    score: float

# 1. 자주 검색되는 증상
@router.get("/symptoms/popular", tags=["symptoms"])
async def get_popular_symptoms():
    # TODO: DB에서 인기 증상 조회
    return {
        "result": ["두통", "발열", "기침", "콧물", "복통"]
    }

# 2. 사용자가 입력한 증상 검색
class SymptomSearchRequest(BaseModel):
    keywords: List[str]

@router.post("/symptoms/search", response_model=List[DrugRecommendation], tags=["symptoms"])
async def search_symptoms(req: SymptomSearchRequest):
    # TODO: 입력된 키워드로 약 추천 로직 수행
    return [
        DrugRecommendation(drug_id=1, drug_name="타이레놀", score=0.95),
        DrugRecommendation(drug_id=2, drug_name="콜대원", score=0.87)
    ]

# 3. 신체 부위 기반 증상 추천
@router.get("/symptoms/by-body-part", tags=["symptoms"])
async def get_symptoms_by_body_part(part: str = Query(..., example="머리")):
    # TODO: part 값으로 관련 증상 리스트 반환
    return {
        "result": ["두통", "눈 통증", "어지러움"]
    }
