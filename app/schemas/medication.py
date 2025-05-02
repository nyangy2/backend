from pydantic import BaseModel

class MedicationSearchRequest(BaseModel):
    product_name: str

class MedicationSearchRequest(BaseModel):
    product_name: str
    company: str

class MedicationDetailResponse(BaseModel):
    product_code: str
    product_name: str
    ingredient_name: str | None = None
    atc_name: str | None = None
