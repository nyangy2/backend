from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.medication import Medication
from typing import List

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
