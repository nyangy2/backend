from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user_model
from app.schemas.mypage import UserInfoResponse, VerifyPasswordRequest, UserUpdateRequest
from app.db.models.user import User

router = APIRouter()

from app.crud import mypage as mypage_crud

@router.get("/info", response_model=UserInfoResponse)
def get_my_info(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_model)
):
    
    return mypage_crud.get_user_info(user)

#@router.post("/verify-password")
def verify_password_endpoint(
    payload: VerifyPasswordRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_model)
):
    if not mypage_crud.verify_user_password(user, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="비밀번호가 일치하지 않습니다.")
    return {
    "code": 200,
    "message": "비밀번호가 확인되었습니다.",
    "verified": True
    }

@router.patch("/edit")
def update_user_info(
    update_data: UserUpdateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_model)
):
    result = mypage_crud.update_user(db, user, update_data)
    return result
