from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.user import User as UserModel
from app.schemas.user import User as UserSchema
from app.db.session import get_db



# 비밀번호 해시용 context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 관련 설정
# .env에서 가져온 값들
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 PasswordBearer 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 비밀번호 해싱
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 현재 로그인된 유저 확인
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명이 유효하지 않습니다.",
    )

    try:
        print("🟡 토큰 디코딩 시작")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("🟢 payload:", payload)

        user_id: str = payload.get("sub")
        print("🔑 user_id:", user_id)

        if user_id is None:
            print("❌ user_id 없음")
            raise credentials_exception

    except JWTError as e:
        print("❌ JWTError:", e)
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    print("🧍 user from DB:", user)

    if not user:
        print("❌ 해당 user_id가 DB에 없음")
        raise credentials_exception

    return UserSchema.from_orm(user)
