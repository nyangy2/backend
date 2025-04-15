from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest, LoginRequest
from app.db.session import get_db
from app.utils.response import standard_response
from app.crud import auth as auth_crud
from app.db.models.user import User

router = APIRouter()

@router.post("/signup")
def signup(user_data: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="비밀번호는 8자 이상이어야 합니다.")

    user = auth_crud.create_user(db, user_data)
    token = auth_crud.create_access_token(data={"sub": str(user.id)})
    return standard_response(
        result={"access_token": token, "token_type": "bearer"},
        code="200",
        message="회원가입이 완료되었습니다."
    )



@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    token = auth_crud.authenticate_user(db, login_data)
    if not token:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    return standard_response(
        result={"access_token": token, "token_type": "bearer"},
        code="200",
        message="로그인에 성공하였습니다."
    )