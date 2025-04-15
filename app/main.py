from fastapi import FastAPI, HTTPException
from app.api.router import api_router
from app.db.session import engine
from app.db.base import Base
from fastapi.exceptions import RequestValidationError
from app.utils.error_handler import (
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)

app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"❌ DB 연결 실패: {e}")

@app.get("/")
def root():
    return {"message": "Hello, FastAPI + Docker!"}

app.include_router(api_router)
