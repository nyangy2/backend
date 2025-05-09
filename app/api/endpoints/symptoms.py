from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.symptom_log import get_popular_symptoms, log_symptom_search
from app.utils.response import standard_response
from app.schemas.user import User as UserSchema
from app.schemas.symptoms import SymptomSearchRequest, DrugRecommendation, SymptomSearchResult
from app.db.models.symptom import Symptom

router = APIRouter()

# 자주 검색되는 증상
@router.get("/popular")
def popular_symptoms(user=Depends(get_current_user), db: Session = Depends(get_db)):
    popular = get_popular_symptoms(db)
    return standard_response(result=popular)




@router.get("/search", response_model=List[SymptomSearchResult])
def search_symptom_candidates(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    results = (
        db.query(Symptom.id, Symptom.name)
        .filter(Symptom.name.ilike(f"%{keyword}%"))
        .order_by(Symptom.name.asc())
        .limit(10)
        .all()
    )
    return [{"id": r.id, "name": r.name} for r in results]


# 사용자가 입력한 증상 검색
@router.post("/search", response_model=List[DrugRecommendation], tags=["symptoms"])
async def search_symptoms(
    req: SymptomSearchRequest,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user)
):
    # 증상 검색 기록 저장
    for symptom in req.symptoms:
        log_symptom_search(db=db, user_id=user.id, symptom=symptom)

    # TODO: AI 약 추천 로직 대신 더미 결과
    return [
        DrugRecommendation(drug_id=1, drug_name="타이레놀", score=0.95),
        DrugRecommendation(drug_id=2, drug_name="콜대원", score=0.87)
    ]

# 신체 부위 기반 증상 추천
@router.get("/by-body-part", tags=["symptoms"])
async def get_symptoms_by_body_part(part: str = Query(..., example="머리")):
    # TODO: part 값으로 관련 증상 리스트 반환
    return {
        "result": ["두통", "눈 통증", "어지러움"]
    }
