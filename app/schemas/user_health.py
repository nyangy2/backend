from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# POST 요청용: keyword 하나만 받음 (자동완성 기반 등록)
class UserDrugCreate(BaseModel):
    item_seq: str

# 응답용: 등록된 약 정보 반환
class UserDrug(BaseModel):
    id: int
    item_seq: str
    item_name: str
    entp_name: str
    atc_code: str | None = None
    main_ingr_eng: str | None = None
    main_item_ingr: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 기준
class UserDrugSimpleResponse2(BaseModel):
    item_seq: str
    item_name: str
    entp_name: str
    morning: bool
    afternoon: bool
    evening: bool
    class Config:
        from_attributes = True
class UserDrugSimpleResponse(BaseModel):
    item_seq: str
    item_name: str
    entp_name: str

    class Config:
        from_attributes = True

#GET 용 
class DrugSearchResult(BaseModel):
    item_seq: str
    item_name: str
    entp_name: str

class DrugTakeStatusUpdate(BaseModel):
    morning: Optional[bool] = None
    afternoon: Optional[bool] = None
    evening: Optional[bool] = None

class DrugTakeStatusUpdateResponse(BaseModel):
    item_seq: str
    morning: Optional[bool] = None
    afternoon: Optional[bool] = None
    evening: Optional[bool] = None

#---------------------------------------------------
#기저질환용

class ConditionSearchResult(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class UserConditionCreate(BaseModel):
    condition_id: int  # 사용자가 선택한 chronic_condition의 id

class UserConditionResponse(BaseModel):
    condition_id: int
    name: str
    class Config:
        from_attributes = True  # SQLAlchemy ORM 연동