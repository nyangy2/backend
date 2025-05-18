from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import base64
import requests
import re

from app.db.session import get_db
from app.db.models.medication import Medication
from app.schemas.image import ImageSearchResult
from app.core.config import settings

router = APIRouter(prefix="/image")

def clean_ocr_text(raw_text: str) -> str:
    cleaned = re.sub(r"\(.*?\)", "", raw_text)
    cleaned = re.sub(r"[^가-힣a-zA-Z0-9\s]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def normalize_text(raw_text: str) -> str:
    # 괄호 제거 + 공백 제거 + 특수문자 제거
    cleaned = re.sub(r"\(.*?\)", "", raw_text)
    cleaned = re.sub(r"[^가-힣a-zA-Z0-9]", "", cleaned)
    return cleaned.strip()

def extract_text_from_image(image_bytes: bytes, api_key: str) -> str:
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    payload = {
        "requests": [{
            "image": {"content": base64_image},
            "features": [{"type": "TEXT_DETECTION"}]
        }]
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="OCR 요청 실패")

    res_json = response.json()
    try:
        return res_json["responses"][0]["textAnnotations"][0]["description"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="텍스트를 인식하지 못했습니다.")

def extract_probable_drug_lines(ocr_text: str) -> list[str]:
    lines = ocr_text.splitlines()
    candidates = []
    for line in lines:
        if any(keyword in line for keyword in ["정", "캡슐", "정제", "mg", "mL", "그램"]):
            candidates.append(clean_ocr_text(line))
    return candidates

@router.post("/scan", response_model=list[ImageSearchResult])
def scan_medication_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_bytes = file.file.read()
    print(f"[DEBUG] 파일명: {file.filename}")
    print(f"[DEBUG] 파일 크기: {len(image_bytes)} bytes")

    raw_text = extract_text_from_image(image_bytes, settings.GOOGLE_VISION_API_KEY)
    print(f"[DEBUG] OCR 결과 원본:\n{raw_text}")

    candidate_lines = extract_probable_drug_lines(raw_text)
    print(f"[DEBUG] 후보 약품명 라인: {candidate_lines}")

    all_results = []

    for keyword in candidate_lines:
        normalized = normalize_text(keyword)
        print(f"[DEBUG] 검색 키워드: '{normalized}'")

        results = (
            db.query(Medication)
            .filter(Medication.item_name.ilike(f"%{normalized}%"))
            .limit(5)
            .all()
        )
        all_results.extend(results)

    # 중복 제거 (item_seq 기준)
    unique_results = {r.item_seq: r for r in all_results}.values()

    print(f"[DEBUG] 최종 반환 약품 수: {len(unique_results)}")
    return list(unique_results)
