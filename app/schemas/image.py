# app/schemas/image.py
from pydantic import BaseModel

class ImageSearchResult(BaseModel):
    item_seq: str
    item_name: str
    entp_name: str
