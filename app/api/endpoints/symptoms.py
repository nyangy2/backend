from fastapi import APIRouter, Query
from typing import List, Optional
from app.schemas.symptoms import SymptomSearchRequest, DrugRecommendation
from app.utils.response import standard_response

router = APIRouter()

# 1. 자주 검색되는 증상
@router.get("/symptoms/popular", tags=["symptoms"])
async def get_popular_symptoms():
     # 실제 DB 연동 전 테스트용 더미 데이터
    symptoms = ["두통", "발열", "기침", "콧물", "더미데이터"]
    return standard_response(result=symptoms)

# 2. 사용자가 입력한 증상 검색
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
