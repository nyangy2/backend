from datetime import datetime, timezone
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# 1. 유효성 검사 오류 (422)
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
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "code": "422",
            "message": error_msg,
            "result": None
        }
    )

# 2. 일반 HTTP 예외 (401, 403, 404 등)
async def http_exception_handler(request: Request, exc: HTTPException):
    # "Not authenticated" → 한글 메시지로 변환
    message = (
        "로그인이 필요합니다."
        if exc.status_code == 401 and exc.detail == "Not authenticated"
        else exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "code": str(exc.status_code),
            "message": message,
            "result": None
        }
    )

# 3. 예기치 못한 서버 에러 (500)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "code": "500",
            "message": "서버 내부 오류가 발생했습니다.",
            "result": None
        }
    )

# 4. 비즈니스 로직 오류 (비밀번호 조건 불일치 등)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "code": "400",
            "message": str(exc),
            "result": None
        }
    )