from pydantic import BaseModel, EmailStr

# 회원가입 요청 모델
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

# 로그인 요청 모델
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 로그인 응답 (JWT 토큰)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
