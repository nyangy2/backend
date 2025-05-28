from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.user_health import UserDrug, UserCondition
from app.db.models.medication import Medication
from app.db.models.chronic_condition import ChronicCondition
from app.schemas.user_health import DrugTakeStatusUpdate, DrugTakeStatusUpdateResponse

def create_user_drug(db: Session, user_id: int, item_seq: str) -> UserDrug:
    #중복 등록 방지
    existing = (
        db.query(UserDrug)
        .filter(UserDrug.user_id == user_id, UserDrug.item_seq == item_seq)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 약입니다.")

    med = db.query(Medication).filter(Medication.item_seq == item_seq).first()
    if not med:
        raise HTTPException(status_code=404, detail="해당 약품을 찾을 수 없습니다.")

    new_drug = UserDrug(
        user_id=user_id,
        item_seq=med.item_seq,
        item_name=med.item_name,
        entp_name=med.entp_name,
        atc_code=med.atc_code,
        main_ingr_eng=med.main_ingr_eng,
        main_item_ingr=med.main_item_ingr
    )
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)
    return new_drug

def get_user_drugs(db: Session, user_id: int) -> list[UserDrug]:
    return (
        db.query(UserDrug)
        .filter(UserDrug.user_id == user_id)
        .order_by(UserDrug.created_at.desc())
        .all()
    )

def delete_user_drug_by_item_seq(db: Session, user_id: int, item_seq: str) -> UserDrug:
    drug = (
        db.query(UserDrug)
        .filter(UserDrug.user_id == user_id, UserDrug.item_seq == item_seq)
        .first()
    )
    if not drug:
        raise HTTPException(status_code=404, detail="해당 약품이 존재하지 않습니다.")

    db.delete(drug)
    db.commit()
    return drug  # 삭제된 객체를 반환

def update_take_status(db: Session, user_id: int, item_seq: str, update_data: DrugTakeStatusUpdate) -> UserDrug:
    drug = (
        db.query(UserDrug)
        .filter(UserDrug.user_id == user_id, UserDrug.item_seq == item_seq)
        .first()
    )
    if not drug:
        raise HTTPException(status_code=404, detail="해당 약품이 존재하지 않습니다.")
    
    if update_data.morning is not None:
        drug.morning = update_data.morning
    if update_data.afternoon is not None:
        drug.afternoon = update_data.afternoon
    if update_data.evening is not None:
        drug.evening = update_data.evening
    
    db.commit()
    db.refresh(drug)
    return DrugTakeStatusUpdateResponse(
        item_seq=drug.item_seq,
        morning=drug.morning,
        afternoon=drug.afternoon,
        evening=drug.evening
    )

#--------------------------------------------

def create_user_condition(db: Session, user_id: int, condition_id: int) -> UserCondition:
    # 중복 등록 방지
    existing = (
        db.query(UserCondition)
        .filter(UserCondition.user_id == user_id, UserCondition.condition_id == condition_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 질환입니다.")

    # chronic_conditions에서 정보 가져오기
    cond = db.query(ChronicCondition).filter(ChronicCondition.id == condition_id).first()
    if not cond:
        raise HTTPException(status_code=404, detail="해당 질환 정보를 찾을 수 없습니다.")

    # 복사 저장
    new_condition = UserCondition(
        user_id=user_id,
        condition_id=condition_id,
        name=cond.name,
        name_eng=cond.name_eng,
        icd_code=cond.icd_code
    )
    db.add(new_condition)
    db.commit()
    db.refresh(new_condition)
    return new_condition


def get_user_conditions(db: Session, user_id: int) -> list[UserCondition]:
    return (
        db.query(UserCondition)
        .filter(UserCondition.user_id == user_id)
        .order_by(UserCondition.created_at.desc())
        .all()
    )

def delete_user_condition(db: Session, user_id: int, condition_id: int) -> UserCondition:
    condition = (
        db.query(UserCondition)
        .filter(UserCondition.user_id == user_id, UserCondition.condition_id == condition_id)
        .first()
    )
    if not condition:
        raise HTTPException(status_code=404, detail="등록된 질환이 없습니다.")

    db.delete(condition)
    db.commit()
    return condition