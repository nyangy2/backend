from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import auth as auth_schemas
from app.db.session import SessionLocal
from app.core.security import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model = auth_schemas.Token)
def signup(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    #DB 저장 생략
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token}

@router.post("/login", response_model= auth_schemas.Token)
def login(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    #비밀번호 검증 생략
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token}