from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.mypage import UserUpdateRequest, UserInfoResponse
from app.core.security import get_password_hash
from app.utils.password import is_valid_password

def get_user_info(user: User) -> UserInfoResponse:
    return UserInfoResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age,
        gender=user.gender,
        provider=user.provider
    )


def verify_user_password(user: User, plain_password: str) -> bool:
    from app.core.security import verify_password
    return verify_password(plain_password, user.hashed_password)


def update_user(db: Session, user: User, update_data: UserUpdateRequest) -> dict:
    updated_fields = {}

    if update_data.name is not None and update_data.name != user.name:
        user.name = update_data.name
        updated_fields["name"] = update_data.name

    if update_data.age is not None and update_data.age != user.age:
        user.age = update_data.age
        updated_fields["age"] = update_data.age

    if update_data.gender is not None and update_data.gender != user.gender:
        user.gender = update_data.gender
        updated_fields["gender"] = update_data.gender

    if updated_fields:
        db.commit()
        db.refresh(user)
        message = "회원 정보가 수정되었습니다."
    else:
        message = "변경된 항목이 없습니다."

    return {
        "message": message,
        "updated_fields": updated_fields,
        "user": UserInfoResponse.model_validate(user)
    }

