from pydantic import BaseModel

# 기본 응답용 (간단하게만 필요한 경우)
class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# 소셜 응답용 (카카오 등에서 추가 필드 포함)
class UserFull(BaseModel):
    id: int
    email: str
    name: str
    provider: str | None = None
    social_id: str | None = None

    class Config:
        from_attributes = True


#증상검색용
class UserWithProfile(User):
    age: int
    gender: str

    
    class Config:
        from_attributes = True