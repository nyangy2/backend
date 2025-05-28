from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.session import SessionLocal  # DB 세션 import 경로 확인
from app.db.models.user_health import UserDrug  # 모델 import 경로 확인
from sqlalchemy import update

def reset_medication_flags():
    db: Session = SessionLocal()
    try:
        db.execute(
            update(UserDrug)
            .values(morning=False, afternoon=False, evening=False)
        )
        db.commit()
        print("✅ Medication flags reset at midnight.")
    except Exception as e:
        print(f"[ERROR] Reset failed: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    scheduler.add_job(reset_medication_flags, 'cron', hour=0, minute=0)  # 매일 00:00에 실행
    scheduler.start()
