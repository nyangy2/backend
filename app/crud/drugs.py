from sqlalchemy.orm import Session
from app.db.models.user_health import UserCondition, UserDrug

def get_user_conditions(db: Session, user_id: int) -> list[UserCondition]:
    return db.query(UserCondition).filter(UserCondition.user_id == user_id).all()

def get_user_drugs(db: Session, user_id: int) -> list[UserDrug]:
    return db.query(UserDrug).filter(UserDrug.user_id == user_id).all()