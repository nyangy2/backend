from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.symptom_log import SymptomSearchLog

def get_popular_symptoms(db: Session, limit: int = 5):
    result = (
        db.query(SymptomSearchLog.symptom, func.count().label("count"))
        .group_by(SymptomSearchLog.symptom)
        .order_by(func.count().desc())
        .limit(limit)
        .all()
    )
    return [row.symptom for row in result]



def log_symptom_search(db: Session, user_id: int, symptom: str):
    log = SymptomSearchLog(user_id=user_id, symptom=symptom)
    db.add(log)
    db.commit()