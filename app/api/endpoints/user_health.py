from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.user_health import UserDrug, UserDrugCreate, UserHealthInfo, UserHealthInfoCreate
from app.crud import user_health as crud_mypage
from app.utils.response import standard_response
from typing import List

router = APIRouter()

#복용약품
@router.get("/drugs", response_model=List[UserDrug])
def read_user_drugs(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_mypage.get_user_drugs(db, current_user.id)

@router.post("/drugs", response_model=UserDrug)
def create_user_drug(
    data: UserDrugCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.create_user_drug(db, current_user.id, data.drug_name)

@router.delete("/drugs/{drug_id}")
def delete_user_drug(drug_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    crud_mypage.delete_user_drug(db, current_user.id, drug_id)
    return standard_response(message="복용약이 삭제되었습니다.")


#기저질환
@router.get("/health-info", response_model=List[UserHealthInfo])
def read_user_health_info(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return crud_mypage.get_user_health_info(db, current_user.id)

@router.post("/health-info", response_model=UserHealthInfo)
def create_user_health_info(
    data: UserHealthInfoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud_mypage.create_user_health_info(db, current_user.id, data.condition)

@router.delete("/health-info/{health_info_id}")
def delete_user_health_info(health_info_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    crud_mypage.delete_user_health_info(db, current_user.id, health_info_id)
    return standard_response(message="기저질환이 삭제되었습니다.")
