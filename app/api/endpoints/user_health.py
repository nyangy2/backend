from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.db.models.medication import Medication
from app.db.models.chronic_condition import ChronicCondition
from app.schemas.user_health import (
    UserDrug,
    DrugTakeStatusUpdate,
    UserDrugCreate,
    DrugSearchResult,
    UserDrugSimpleResponse,
    UserDrugSimpleResponse2,
    UserConditionCreate,
    UserConditionResponse,
    ConditionSearchResult,
    DrugTakeStatusUpdateResponse
)
from app.crud import user_health as crud_mypage
from typing import List

router = APIRouter()

# 복용약 등록
@router.post("/drugs", response_model=UserDrugSimpleResponse)
def create_user_drug(
    data: UserDrugCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.create_user_drug(
        db, current_user.id, data.item_seq
    )

@router.get("/drugs/search", response_model=List[DrugSearchResult])
def search_user_drug_candidates(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    results = (
        db.query(Medication.item_seq, Medication.item_name, Medication.entp_name)
        .filter(Medication.item_name.ilike(f"{keyword}%"))
        .order_by(Medication.item_name.asc())
        .limit(10)
        .all()
    )

    return [
        DrugSearchResult(
            item_seq=r.item_seq,
            item_name=r.item_name,
            entp_name=r.entp_name
        )
        for r in results
    ]

@router.get("/drugs", response_model=List[UserDrugSimpleResponse2])
def read_user_drugs(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.get_user_drugs(db, current_user.id)

@router.delete("/drugs/{item_seq}", response_model=UserDrugSimpleResponse)
def delete_user_drug(
    item_seq: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.delete_user_drug_by_item_seq(db, current_user.id, item_seq)

@router.patch("/drugs/{item_seq}", response_model=DrugTakeStatusUpdateResponse)
def patch__take_status(
    item_seq: str,
    update_data: DrugTakeStatusUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
    ):
    return crud_mypage.update_take_status(db, current_user.id, item_seq, update_data)



#------------------------------------------------------------

# 사용자 질환 등록
@router.post("/conditions", response_model=UserConditionResponse)
def create_user_condition(
    data: UserConditionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.create_user_condition(db, current_user.id, data.condition_id)


# 사용자 질환 목록 조회
@router.get("/conditions", response_model=List[UserConditionResponse])
def get_user_conditions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.get_user_conditions(db, current_user.id)


# 사용자 질환 삭제
@router.delete("/conditions/{condition_id}", response_model=UserConditionResponse)
def delete_user_condition(
    condition_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.delete_user_condition(db, current_user.id, condition_id)


@router.get("/conditions/list", response_model=List[ConditionSearchResult])
def list_all_chronic_conditions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    results = (
        db.query(ChronicCondition.id, ChronicCondition.name)
        .order_by(ChronicCondition.id.asc())
        .all()
    )
    return [ConditionSearchResult(id=r.id, name=r.name) for r in results]



#@router.get("/conditions/search", response_model=List[ConditionSearchResult])
def search_chronic_conditions(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    results = (
        db.query(ChronicCondition.id, ChronicCondition.name)
        .filter(ChronicCondition.name.ilike(f"{keyword}%"))
        .order_by(ChronicCondition.name.asc())
        .limit(10)
        .all()
    )

    return [ConditionSearchResult(id=r.id, name=r.name) for r in results]