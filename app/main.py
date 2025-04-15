from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi

from app.api.router import api_router
from app.db.session import engine
from app.db.base import Base
from app.utils.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)

app = FastAPI()

# Swagger Authorize 버튼을 위한 OpenAPI 스키마 설정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="상비약 추천 서비스",
        version="1.0.0",
        description="AI 기반 사용자 맞춤 상비약 검색 시스템",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

#예외 핸들러러
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f" DB 연결 실패: {e}")

@app.get("/")
def root():
    return {"message": "Hello, FastAPI + Docker!"}

app.include_router(api_router)
