from pydantic import BaseModel

class Drug(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
