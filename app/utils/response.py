from fastapi.responses import JSONResponse
from fastapi import HTTPException
from datetime import datetime, timezone

def standard_response(result=None, code="COMMON200", message="요청에 성공하였습니다."):
    return JSONResponse(content={
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code": code,
        "message": message,
        "result": result
    })

def standard_exception(status_code: int, code: str, message: str):
    raise HTTPException(
        status_code=status_code,
        detail={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "code": code,
            "message": message,
            "result": None
        }
    )
