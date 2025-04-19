from pydantic import BaseModel

class Drug(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
