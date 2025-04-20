from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user, get_current_user_model
from app.db.models.user import User as UserModel
from app.schemas.mypage import UpdatePasswordRequest, UpdateNameRequest
from app.crud.mypage import update_password, update_name

router = APIRouter()

@router.patch("/password", summary="비밀번호 변경")
def change_password(
    body: UpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_model)
):
    success = update_password(db, current_user, body.current_password, body.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")
    return {"message": "비밀번호가 성공적으로 변경되었습니다."}

@router.patch("/name", summary="이름 변경")
def change_name(
    body: UpdateNameRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_model)
):
    update_name(db, current_user, body.new_name)
    return {"message": "이름이 성공적으로 변경되었습니다."}
