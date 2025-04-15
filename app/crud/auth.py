# app/crud/auth.py

from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status

# 회원가입
def create_user(db: Session, user_data: SignupRequest):
    # 이메일 중복 확인
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    hashed_pw = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_pw
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 로그인
def authenticate_user(db: Session, login_data: LoginRequest):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="잘못된 이메일 또는 비밀번호입니다.")

    # 토큰 생성
    token = create_access_token(data={"sub": str(user.id)})
    return token
