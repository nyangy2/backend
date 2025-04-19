from sqlalchemy.orm import Session
from app.db.models.mypage import UserDrug, UserHealthInfo
from fastapi import HTTPException

def get_user_drugs(db: Session, user_id: int):
    return db.query(UserDrug).filter(UserDrug.user_id == user_id).all()

def get_user_health_info(db: Session, user_id: int):
    return db.query(UserHealthInfo).filter(UserHealthInfo.user_id == user_id).all()

def create_user_health_info(db: Session, user_id: int, condition: str):
    existing = db.query(UserHealthInfo).filter_by(user_id=user_id, condition=condition).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 기저질환입니다.")

    db_info = UserHealthInfo(user_id=user_id, condition=condition)
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

def delete_user_health_info(db: Session, user_id: int, health_info_id: int):
    info = db.query(UserHealthInfo).filter(
        UserHealthInfo.id == health_info_id,
        UserHealthInfo.user_id == user_id
    ).first()

    if not info:
        raise HTTPException(status_code=404, detail="해당 기저질환이 존재하지 않거나 권한이 없습니다.")

    db.delete(info)
    db.commit()

def create_user_drug(db: Session, user_id: int, drug_name: str):
    existing = db.query(UserDrug).filter_by(user_id=user_id, drug_name=drug_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 복용약입니다.")
    
    new = UserDrug(user_id=user_id, drug_name=drug_name)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

def delete_user_drug(db: Session, user_id: int, drug_id: int):
    drug = db.query(UserDrug).filter(UserDrug.id == drug_id, UserDrug.user_id == user_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="해당 복용약이 존재하지 않거나 권한이 없습니다.")
    db.delete(drug)
    db.commit()