from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
