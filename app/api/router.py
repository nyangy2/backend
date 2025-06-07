from fastapi import APIRouter, Depends
from app.api.endpoints import auth, auth_social, symptoms, image, user_health, mypage, medication, drug_info
from app.core.security import get_current_user

api_router = APIRouter()

#일반 인증 
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

#소셜 로그인
api_router.include_router(auth_social.router, prefix="/auth", tags=["auth-social"])

#증상 검색
api_router.include_router(
    symptoms.router, prefix="/symptoms", tags=["symptoms"],
    dependencies=[Depends(get_current_user)]
)

api_router.include_router(
    user_health.router, prefix="/user_health", tags=["user_health"],
    dependencies=[Depends(get_current_user)])

api_router.include_router(
    mypage.router, prefix="/mypage", tags=["mypage"],
    dependencies=[Depends(get_current_user)])

api_router.include_router(
    drug_info.router, prefix="/drug_info", tags=["drug_info"],
    Dependencies=[Depends(get_current_user)])

api_router.include_router(medication.router, prefix="/medications", tags=["medications"])

api_router.include_router(
    image.router, prefix="/image", tags=["image"],
    dependencies=[Depends(get_current_user)])