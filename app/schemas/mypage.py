from pydantic import BaseModel, Field, constr

class UpdatePasswordRequest(BaseModel):
    current_password: str = Field(..., example="oldpassword123")
    new_password: constr(min_length=8) = Field(..., example="newpassword456")

class UpdateNameRequest(BaseModel):
    new_name: str = Field(..., example="홍길동")
