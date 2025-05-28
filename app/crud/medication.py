from sqlalchemy.orm import Session
from app.db.models.medication import Medication
from app.db.models.user_health import UserDrug
from app.db.models.drug_interactions import DrugInteraction
from typing import List
import itertools
from app.schemas.medication import CondensedInteractionItem

def get_ingredients_for_item_seqs(db: Session, item_seqs: List[str]) -> dict:
    meds = (
        db.query(Medication.item_seq, Medication.item_name, Medication.main_ingr_eng)
        .filter(Medication.item_seq.in_(item_seqs))
        .all()
    )
    result = {}
    for item_seq, item_name, ingr_str in meds:
        ingredients = [i.strip() for i in (ingr_str or "").split("/") if i.strip()]
        result[item_seq] = {
            "item_name": item_name,
            "ingredients": ingredients
        }
    return result

def get_user_medication_ids(db: Session, user_id: int) -> List[str]:
    return [
        row.item_seq for row in
        db.query(UserDrug.item_seq).filter(UserDrug.user_id == user_id).all()
    ]

def check_interactions_for_user(
    db: Session,
    user_id: int,
    new_item_seq: str
) -> List[DrugInteraction]:
    current_item_seqs = get_user_medication_ids(db, user_id)
    all_item_seqs = current_item_seqs + [new_item_seq]
    ingredient_map = get_ingredients_for_item_seqs(db, all_item_seqs)

    new_info = ingredient_map.get(new_item_seq)
    if not new_info:
        return []

    new_ingredients = new_info["ingredients"]
    interactions = []

    for cur_seq in current_item_seqs:
        cur_info = ingredient_map.get(cur_seq)
        if not cur_info:
            continue

        for a, b in itertools.product(cur_info["ingredients"], new_ingredients):
            if a == b:
                interactions.append(DrugInteraction(
                    ingredient_a=a,
                    product_a=cur_info["item_name"],
                    manufacturer_a="",
                    ingredient_b=b,
                    product_b=new_info["item_name"],
                    manufacturer_b="",
                    detail=f"'{a}' 성분이 중복됩니다. 중복 복용 시 과용 위험이 있습니다."
                ))
                continue

            results1 = db.query(DrugInteraction).filter(
                DrugInteraction.ingredient_a == a,
                DrugInteraction.ingredient_b == b
            ).all()

            results2 = db.query(DrugInteraction).filter(
                DrugInteraction.ingredient_a == b,
                DrugInteraction.ingredient_b == a
            ).all()

            interactions.extend(results1)
            interactions.extend(results2)

    return interactions

def check_condensed_interactions_for_user(
    db: Session,
    user_id: int,
    new_item_seq: str
) -> List[CondensedInteractionItem]:
    current_item_seqs = get_user_medication_ids(db, user_id)
    all_item_seqs = current_item_seqs + [new_item_seq]
    ingredient_map = get_ingredients_for_item_seqs(db, all_item_seqs)

    new_info = ingredient_map.get(new_item_seq)
    if not new_info:
        return []

    new_ingredients = new_info["ingredients"]
    results = []

    for cur_seq in current_item_seqs:
        cur_info = ingredient_map.get(cur_seq)
        if not cur_info:
            continue

        matched = False
        for a, b in itertools.product(cur_info["ingredients"], new_ingredients):
            if a == b:
                results.append(CondensedInteractionItem(
                    product_a=cur_info["item_name"],
                    manufacturer_a="",
                    interaction_type="중복성분",
                    detail=f"{a} 성분이 중복됩니다. 중복 복용 시 과용 위험이 있습니다."
                ))
                matched = True
                break

            # ilike로 느슨한 비교 추가
            a_clean = a.lower().strip()
            b_clean = b.lower().strip()

            r1 = db.query(DrugInteraction).filter(
                DrugInteraction.ingredient_a.ilike(f"%{a_clean}%"),
                DrugInteraction.ingredient_b.ilike(f"%{b_clean}%")
            ).first()

            r2 = db.query(DrugInteraction).filter(
                DrugInteraction.ingredient_a.ilike(f"%{b_clean}%"),
                DrugInteraction.ingredient_b.ilike(f"%{a_clean}%")
            ).first()

            picked = r1 or r2
            if picked:
                results.append(CondensedInteractionItem(
                    product_a=cur_info["item_name"],
                    manufacturer_a="",
                    interaction_type="병용금기",
                    detail=picked.detail
                ))
                matched = True
                break

    return results