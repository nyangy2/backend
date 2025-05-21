from fastapi import APIRouter, Depends, Query
from app.core.security import get_current_user
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.medication import Medication
from app.ai.drug_interaction import check_interactions_openai
from app.db.models.user import User
from typing import List
from app.schemas.medication import (
    InteractionCheckRequest,
    InteractionCheckResponse,
    InteractionItem,
    CondensedInteractionResponse
)
from app.crud.medication import check_interactions_for_user, check_condensed_interactions_for_user

router = APIRouter()

@router.get("/search")
def search_medications(
    prefix: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    results = (
        db.query(Medication.item_seq, Medication.item_name)
        .filter(Medication.item_name.ilike(f"{prefix}%"))
        .limit(10)
        .all()
    )
    return [{"item_seq": r.item_seq, "item_name": r.item_name} for r in results]




@router.post("/check-interaction", response_model=CondensedInteractionResponse)
def check_interaction(
    request: InteractionCheckRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # GPT 기반 분석 함수로 위임
    response = check_interactions_openai(user.id, request.new_medication_id, db)
    return response