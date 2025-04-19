from fastapi import APIRouter, Depends
from app.api.endpoints import auth, symptoms, drugs, image, user_health
from app.core.security import get_current_user

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(
    symptoms.router, prefix="/symptoms", tags=["symptoms"],
    dependencies=[Depends(get_current_user)]
)
api_router.include_router(drugs.router, prefix="/drugs", tags=["drugs"])
#api_router.include_router(image.router, prefix="/image", tags=["image"])
api_router.include_router(
    user_health.router, prefix="/user_health", tags=["user_health"],
    dependencies=[Depends(get_current_user)])