from sqlalchemy.orm import Session
from app.db.models.user import User as UserModel
from app.core.security import verify_password, get_password_hash

def update_password(db: Session, user: UserModel, current_password: str, new_password: str):
    if not verify_password(current_password, user.hashed_password):
        return False
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    return True

def update_name(db: Session, user: UserModel, new_name: str):
    user.name = new_name
    db.commit()
    return True
