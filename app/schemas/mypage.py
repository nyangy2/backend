from pydantic import BaseModel, Field

class UpdatePasswordRequest(BaseModel):
    current_password: str = Field(..., example="asdf1234")
    new_password: str = Field(..., example="abc12345")

class UpdateNameRequest(BaseModel):
    new_name: str = Field(..., example="홍길동")
