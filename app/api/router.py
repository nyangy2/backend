from fastapi import APIRouter
from app.api.endpoints import auth, drugs, image, mypage

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
#api_router.include_router(drugs.router, prefix="/drugs", tags=["drugs"])
#api_router.include_router(image.router, prefix="/image", tags=["image"])
#api_router.include_router(mypage.router, prefix="/mypage", tags=["mypage"])