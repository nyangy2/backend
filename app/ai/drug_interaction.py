from app.db.models.user_health import UserDrug
from app.db.models.medication import Medication
from app.schemas.medication import CondensedInteractionItem, CondensedInteractionResponse, AlternativeDrug
from sqlalchemy.orm import Session
from sqlalchemy import or_
import openai
import json
import re  # ← 추가됨

def check_interactions_openai(user_id: int, new_med_id: str, db: Session) -> CondensedInteractionResponse:
    # 1. 현재 복용 중인 약 이름 가져오기
    current_item_names = (
        db.query(Medication.item_name)
        .join(UserDrug, Medication.item_seq == UserDrug.item_seq)
        .filter(UserDrug.user_id == user_id)
        .distinct()
        .all()
    )
    current_names = [row[0] for row in current_item_names]
    print("[DEBUG] 현재 복용 약:", current_names)

    # 2. 새로 복용할 약 이름
    new_med = db.query(Medication.item_name).filter(Medication.item_seq == new_med_id).first()
    if not new_med:
        raise ValueError(f"해당 item_seq '{new_med_id}'에 해당하는 약품을 찾을 수 없습니다.")
    new_med_name = new_med[0]
    print("[DEBUG] 새 약품명:", new_med_name)

    # 3. 프롬프트 생성
    prompt = generate_gpt_prompt(current_names, new_med_name)
    print("[DEBUG] GPT 프롬프트:\n", prompt)

    # 4. GPT 호출
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    result_text = completion["choices"][0]["message"]["content"]
    print("[DEBUG] GPT 응답 원문:\n", result_text)

    # 5. 응답 전처리: 백틱 제거
    cleaned_text = re.sub(r"```[a-z]*\n?", "", result_text).strip()
    print("[DEBUG] 정제된 응답:\n", cleaned_text)

    # 6. JSON 파싱
    parsed = json.loads(cleaned_text)
    print("[DEBUG] 파싱된 JSON:", parsed)

    # 7. 상호작용 정보 파싱
    interactions = [
        CondensedInteractionItem(
            product_a=item["with"],
            manufacturer_a="",
            interaction_type=item["level"],
            detail=item["description"]
        )
        for item in parsed.get("interactions", [])
    ]
    print("[DEBUG] 상호작용 파싱 결과:", interactions)

    # 8. 성분 추천 파싱 및 대체약 조회
    alt_ingredients = parsed.get("alternative_ingredients", [])
    print("[DEBUG] 추천 성분 (영문):", alt_ingredients)

    alt_meds = db.query(Medication).filter(
        Medication.etc_otc_code == "일반의약품",
        or_(*[Medication.main_ingr_eng.ilike(f"%{ingr}%") for ingr in alt_ingredients])
    ).limit(20).all()
    print("[DEBUG] DB에서 검색된 대체약품:", [(m.item_name, m.main_ingr_eng) for m in alt_meds])
    
    grouped = {}
    for med in alt_meds:
        for ingr in alt_ingredients:
            if ingr.lower() in (med.main_ingr_eng or "").lower():
                grouped.setdefault(ingr, []).append(med)

    alternative_drugs = []
    for ingr, meds in grouped.items():
        for med in meds[:2]:
            alternative_drugs.append(AlternativeDrug(
            item_name=med.item_name,
            item_seq=med.item_seq,
            manufacturer=med.entp_name,
            ingredient=ingr
        ))
    print("[DEBUG] 최종 추천 약품:", alternative_drugs)

    # 9. 최종 응답
    return CondensedInteractionResponse(
        interactions=interactions,
        alternative_drugs=alternative_drugs
    )

def generate_gpt_prompt(current_drugs: list[str], new_drug: str) -> str:
    return f"""
현재 사용자가 복용 중인 약품 목록은 다음과 같습니다:
{', '.join(current_drugs)}.

사용자가 추가로 복용하려는 약품은 "{new_drug}"입니다.

아래의 모든 기존 약품 각각과 '{new_drug}' 간 상호작용 여부를 **빠짐없이 모두 평가**해 주세요.

각 약품과의 관계를 아래의 JSON 형식으로 정리해주세요:

{{
  "interactions": [
    {{
      "with": "기존약품명",
      "level": "중복성분 | 병용금기 | 주의 | 안전 중 택1",
      "description": "간단한 설명"
    }},
    ...
  ],
  "alternative_ingredients": [
    "영문 성분명1",
    "영문 성분명2"
  ]
}}

**주의사항**:
- 모든 기존 약품과의 상호작용 결과를 빠짐없이 하나씩 작성해주세요.
- 'alternative_ingredients' 항목에는 추천하는 **영문 성분명만** 나열해주세요. (예: acetaminophen, ibuprofen)
- 응답은 반드시 위 JSON 형식으로만 출력하고, 불필요한 설명이나 ```json 같은 마크다운 기호는 포함하지 마세요.
"""
