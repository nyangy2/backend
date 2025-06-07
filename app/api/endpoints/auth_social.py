from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.db.models.user import User
from app.crud import auth as auth_crud
from app.utils.user import get_current_user_model
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


    # 로그인 성공 후 프론트로 토큰 전달 (쿼리 파라미터)
    redirect_url = f"{settings.FRONTEND_REDIRECT_URL}/login/success?token={token}"
    return RedirectResponse(url=redirect_url)

    # 테스트용 JSON 응답 (임시로 redirect 대신 사용)
    #return {
    #    "user": UserFull.model_validate(user),
    #    "token": token
    #}

#네이버
@router.get("/naver/callback")
async def naver_callback(code: str, state: str, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://nid.naver.com/oauth2.0/token",
            params={
                "grant_type": "authorization_code",
                "client_id": settings.NAVER_CLIENT_ID,
                "client_secret": settings.NAVER_CLIENT_SECRET,
                "code": code,
                "state": state
            }
        )

    if token_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="네이버 토큰 요청 실패")

    access_token = token_resp.json().get("access_token")

    # 2. 사용자 정보 요청
    async with httpx.AsyncClient() as client:
        profile_resp = await client.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

    if profile_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="네이버 사용자 정보 요청 실패")

    user_info = profile_resp.json().get("response", {})
    naver_id = str(user_info.get("id"))
    email = user_info.get("email", f"{naver_id}@naver.com")
    name = user_info.get("name", "네이버사용자")

    # 3. 기존 사용자 확인 or 회원가입
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        user = auth_crud.create_user_by_social(
            db=db,
            email=email,
            provider="naver",
            social_id=naver_id,
            name=name
        )
    else:
        user = existing_user

    # 4. JWT 발급
    token = auth_crud.create_access_token(data={"sub": str(user.id)})

    # 5. 응답
    redirect_url = (
    f"{settings.FRONTEND_REDIRECT_URL}/login/success"
    f"?token={token}&name={user.name}&email={user.email}"
    )
    return RedirectResponse(url=redirect_url)
