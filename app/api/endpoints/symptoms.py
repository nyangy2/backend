from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import get_db
from app.core.security import get_current_user
from app.crud.symptom_log import get_popular_symptoms, log_symptom_search
from app.utils.response import standard_response
from app.schemas.user import User as UserSchema
from app.db.models.user import User as UserModel
from app.schemas.symptoms import SymptomSearchRequest, DrugRecommendation, SymptomSearchResult
from app.db.models.symptom import Symptom
from app.db.models.medication import Medication
from app.db.models.user import User
from app.ai.drug_recommender import ai_suggest_drug_list, normalize, expand_ingredient_keywords
from app.db.models.user_health import UserCondition, UserDrug
from app.crud.drugs import get_user_conditions, get_user_drugs

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
        db.query(Symptom.id, Symptom.name, Symptom.name_eng)
        .filter(Symptom.name.ilike(f"%{keyword}%"))
        .order_by(Symptom.name.asc())
        .limit(10)
        .all()
    )
    return [{"id": r.id, "name": r.name, "name_eng" : r.name_eng} for r in results]


# 사용자가 입력한 증상 검색
@router.post("/search", response_model=List[DrugRecommendation])
async def search_symptoms(
    req: SymptomSearchRequest,
    db: Session = Depends(get_db),
    user: UserSchema = Depends(get_current_user)
):
    # ✅ 1. 증상 검색 기록 저장
    for symptom in req.symptoms:
        log_symptom_search(db=db, user_id=user.id, symptom=symptom)

    db_user = db.query(UserModel).filter(UserModel.id == user.id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    # 사용자 기저질환 및 복용약 정보 조회
    user_conditions = get_user_conditions(db, user.id)
    user_drugs = get_user_drugs(db, user.id)

    condition_names = [cond.name_eng or cond.name for cond in user_conditions]
    current_ingredients = [drug.main_ingr_eng for drug in user_drugs if drug.main_ingr_eng]



    #  AI 추천 성분 리스트 호출
    ingredients = ai_suggest_drug_list(
        symptoms=req.symptoms,
        diseases=condition_names,
        current_drugs=current_ingredients,
        age=db_user.age,
        gender=db_user.gender
    )

    if not ingredients:
        return []

    # 1. 추천된 성분을 normalize
    normalized_ingredients = [normalize(i) for i in ingredients]

    # 2. 동의어 확장
    search_keywords = expand_ingredient_keywords(normalized_ingredients)

    # 성분명 기반 약품 조회
    matching_drugs = (
        db.query(Medication)
        .filter(
            Medication.etc_otc_code != "전문의약품",
            or_(*[Medication.main_ingr_eng.ilike(f"%{kw}%") for kw in search_keywords])
        )
        .limit(10)
        .all()
    )

    # ✅ 6. 응답 구성
    return [
        DrugRecommendation(
            drug_id=drug.item_seq,
            drug_name=drug.item_name,
            entp_name=drug.entp_name or ""
        ) for drug in matching_drugs
    ]
