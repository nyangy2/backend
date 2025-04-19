from pydantic import BaseModel
from typing import List
from datetime import datetime

class UserDrugCreate(BaseModel):
    drug_name: str

class UserDrug(UserDrugCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserHealthInfoCreate(BaseModel):
    condition: str

class UserHealthInfo(UserHealthInfoCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
