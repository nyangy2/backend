from fastapi import APIRouter, Depends, Query, HTTPException
import httpx
import os
from typing import List
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.drugs import DrugSearchResult

router = APIRouter()

@router.get("/search", response_model=List[DrugSearchResult])
async def search_drug_info(
    name: str = Query(..., description="제품명 키워드 (예: 타이레놀)"),
    db: Session = Depends(get_db),
    #current_user=Depends(get_current_user) 로그인 한 유저만
):
    api_key = os.getenv("MFDS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API 키가 설정되지 않았습니다.")

    url = "http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList"
    params = {
        "serviceKey": api_key,
        "itemName": name,
        "type": "json",
        "pageNo": 1,
        "numOfRows": 10
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="식약처 API 호출 실패")

    data = response.json()
    header = data.get("header", {})
    if header.get("resultCode") != "00":
        raise HTTPException(status_code=502, detail=f"식약처 API 오류: {header.get('resultMsg')}")

    items = data.get("body", {}).get("items", [])
    if not items:
        return []

    results = []
    for item in items:
        results.append(DrugSearchResult(
            product_name=item.get("itemName"),
            manufacturer=item.get("entpName"),
            efficacy=item.get("efcyQesitm"),
            use_method=item.get("useMethodQesitm"),
            warning=item.get("atpnWarnQesitm"),
            caution=item.get("atpnQesitm"),
            interaction=item.get("intrcQesitm"),
            side_effect=item.get("seQesitm"),
            storage_method=item.get("depositMethodQesitm"),
            image=item.get("itemImage"),
            open_date=item.get("openDe")
        ))

    return results
