from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.db.models.user import User
from app.crud import auth as auth_crud
from app.utils.user import get_current_user_model  # ⚠️ 이 함수 너가 만든 거
from app.schemas.user import UserFull

router = APIRouter()

@router.get("/kakao/callback")
async def kakao_callback(code: str, db: Session = Depends(get_db)):
    # 1. 액세스 토큰 요청
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_CLIENT_ID,
                "redirect_uri": settings.KAKAO_REDIRECT_URI,
                "code": code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="카카오 토큰 요청 실패")

    access_token = token_resp.json().get("access_token")

    # 2. 사용자 정보 요청
    async with httpx.AsyncClient() as client:
        profile_resp = await client.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

    if profile_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="카카오 사용자 정보 요청 실패")

    user_info = profile_resp.json()

    # 3. 필요한 정보 추출
    kakao_id = str(user_info.get("id"))
    kakao_account = user_info.get("kakao_account", {})
    email = kakao_account.get("email", f"{kakao_id}@kakao.com")
    profile = kakao_account.get("profile", {})
    name = profile.get("nickname", "카카오사용자")

    # 4. 기존 사용자 여부 확인
    existing_user = db.query(User).filter(User.email == email).first()

    if not existing_user:
        # 소셜 회원가입
        user = auth_crud.create_user_by_social(
            db=db,
            email=email,
            provider="kakao",
            social_id=kakao_id,
            name=name
        )
    else:
        user = existing_user

    # 5. JWT 발급
    token = auth_crud.create_access_token(data={"sub": str(user.id)})

    # 6. 응답 통일
    return {
        "user": UserFull.model_validate(user),
        "token": token
    }
