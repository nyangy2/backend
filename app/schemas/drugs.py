from pydantic import BaseModel
from typing import Optional


class DrugSearchResult(BaseModel):
    product_name: Optional[str]         # 제품명
    manufacturer: Optional[str]         # 업체명
    efficacy: Optional[str]             # 효능·효과
    use_method: Optional[str]           # 복용법
    warning: Optional[str]              # 주의사항(경고)
    caution: Optional[str]              # 주의사항(일반)
    interaction: Optional[str]          # 상호작용
    side_effect: Optional[str]          # 부작용
    storage_method: Optional[str]       # 보관방법
    image: Optional[str]                # 제품 이미지 URL
    open_date: Optional[str]            # 공개일자 (yyyymmdd)

    class Config:
        from_attributes = True