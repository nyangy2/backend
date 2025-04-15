from datetime import datetime

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_detail = exc.errors()[0] if exc.errors() else {}
    raw_msg = error_detail.get("msg", "입력값이 유효하지 않습니다.")

    
    if "valid email address" in raw_msg:
        error_msg = "이메일 형식이 올바르지 않습니다."
    else:
        error_msg = raw_msg

    return JSONResponse(
        status_code=422,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "code": "422",
            "message": error_msg,
            "result": None
        }
    )

# FastAPI의 HTTPException → 401, 403, 404 등
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "code": str(exc.status_code),
            "message": exc.detail,
            "result": None
        }
    )

# 기타 알 수 없는 오류 → 500
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "code": "500",
            "message": "서버 내부 오류가 발생했습니다.",
            "result": None
        }
    )

