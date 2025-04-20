from app.schemas.user import User as UserSchema
from app.db.models.user import User

def get_current_user_model(user: User) -> UserSchema:
    return UserSchema.model_validate(user)
