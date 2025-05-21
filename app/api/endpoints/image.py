from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import base64, requests, re

from app.db.session import get_db
from app.db.models.medication import Medication
from app.schemas.image import ImageSearchResult
from app.core.config import settings
from app.ai.drug_refiner import refine_ocr_lines_with_gpt

router = APIRouter()

def extract_text_from_image(image_bytes: bytes, api_key: str) -> str:
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    payload = {
        "requests": [{"image": {"content": base64_image}, "features": [{"type": "TEXT_DETECTION"}]}]
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="OCR 요청 실패")
    try:
        return response.json()["responses"][0]["textAnnotations"][0]["description"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=400, detail="텍스트를 인식하지 못했습니다.")


def normalize_drug_name(name: str) -> str:
    # '레보살탄정 5/160mg' → '레보살탄정'
    # 숫자, mg, 용량정보 제거
    name = re.sub(r"\s*\d+(\s*[/x×]\s*\d+)?\s*mg", "", name, flags=re.IGNORECASE)
    name = re.sub(r"[^가-힣a-zA-Z0-9]", "", name)
    return name.strip()


@router.post("/scan", response_model=list[ImageSearchResult])
def scan_medication_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = file.file.read()
    raw_text = extract_text_from_image(image_bytes, settings.GOOGLE_VISION_API_KEY)
    print(f"[DEBUG] OCR 원문:\n{raw_text}")

    lines = raw_text.splitlines()
    candidate_lines = [line for line in lines if any(k in line for k in ["정", "캡슐", "mg"])]

    if not candidate_lines:
        print("[DEBUG] 후보 약품 라인이 없습니다.")
        return []

    print(f"[DEBUG] 후보 약품 라인: {candidate_lines}")

    # GPT로 일괄 정제
    refined_names = refine_ocr_lines_with_gpt(candidate_lines)
    print(f"[DEBUG] GPT 정제 결과: {refined_names}")

    refined_names = [name for name in refined_names if name != "제외"]

    all_results = []
    for name in refined_names:
        normalized = normalize_drug_name(name)
        print(f"[DEBUG] DB 검색 키워드: {normalized}")

        results = (
            db.query(Medication)
            .filter(Medication.item_name.ilike(f"%{normalized}%"))
            .limit(5)
            .all()
        )
        all_results.extend(results)

    unique_results = {r.item_seq: r for r in all_results}.values()
    print(f"[DEBUG] 최종 반환 약품 수: {len(unique_results)}")
    return list(unique_results)


