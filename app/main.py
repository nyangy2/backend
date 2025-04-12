from fastapi import FastAPI
from app.api.router import api_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI()

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
