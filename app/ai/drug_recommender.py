import openai
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

# ✅ 오타 및 표기 정규화 사전
SPELLING_CORRECTIONS = {
    "acetaminjson": "acetaminophen",
    "acetaminophin": "acetaminophen",
    "phenylephrine hydrochloride": "phenylephrine",
    "pseudoephedrine hydrochloride": "pseudoephedrine",
    "pseudo-ephedrine": "pseudoephedrine",
    "chlorpheniramine maleate": "chlorpheniramine",
    "pheniramine maleate": "chlorpheniramine",
    "chlorpheniramin": "chlorpheniramine",
    "paracetamol": "acetaminophen",  # ✅ 유럽식 이름
    # 필요시 계속 추가
}

# ✅ 동의어 확장 사전: 표준 성분명 → DB 검색용 이름들
INGREDIENT_SYNONYMS = {
    "acetaminophen": ["acetaminophen", "paracetamol"],
    "chlorpheniramine": ["chlorpheniramine", "chlorpheniramine maleate", "pheniramine maleate"],
    "pseudoephedrine": ["pseudoephedrine", "pseudoephedrine hydrochloride"],
    "phenylephrine": ["phenylephrine", "phenylephrine hydrochloride"],
    # 계속 확장 가능
}

# ✅ 성분 정규화 함수
def normalize(name: str) -> str:
    name = name.lower().strip()
    return SPELLING_CORRECTIONS.get(name, name)

# ✅ 복합 성분 분해 및 정규화
def split_and_normalize(ingredient_field: str) -> set[str]:
    return {normalize(part) for part in ingredient_field.split("/")}

# ✅ 중복 필터링
def filter_duplicate_ingredients(recommended: list[str], current: list[str]) -> list[str]:
    normalized_current = set()
    for c in current:
        normalized_current.update(split_and_normalize(c))
    return [r for r in recommended if normalize(r) not in normalized_current]

# ✅ DB 검색용 동의어 확장
def expand_ingredient_keywords(normalized_ingredients: list[str]) -> list[str]:
    expanded = set()
    for ing in normalized_ingredients:
        synonyms = INGREDIENT_SYNONYMS.get(ing, [ing])
        expanded.update(synonyms)
    return list(expanded)

# ✅ GPT 호출
def generate_answer_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response['choices'][0]['message']['content'].strip()

# ✅ 쉼표로 성분 리스트 파싱
def get_clean_drug_list(raw_text: str) -> list[str]:
    return [item.strip() for item in raw_text.split(",") if item.strip()]

# ✅ 전체 파이프라인
def ai_suggest_drug_list(
    symptoms: list[str],
    diseases: list[str],
    current_drugs: list[str],
    age: int,
    gender: str
) -> list[str]:
    symptom_str = ", ".join(symptoms) or "none"
    disease_str = ", ".join(diseases) or "none"
    current_str = ", ".join(current_drugs) or "none"
    gender_text = "male" if gender.upper() == "M" else "female"

    prompt = (
        f"The patient is a {age}-year-old {gender_text} experiencing the following symptoms: {symptom_str}. "
        f"They have the following pre-existing conditions: {disease_str}. "
        f"They are currently taking: {current_str}. "
        f"Recommend a list of safe over-the-counter drug ingredients. "
        f"Do not include any explanations or categories. Output only the ingredient names, separated by commas."
    )

    print(f"📝 GPT Prompt: {prompt}")

    try:
        gpt_answer = generate_answer_gpt(prompt)
        print(f"💬 GPT Answer: {gpt_answer}")
        recommended = get_clean_drug_list(gpt_answer)
        print(f"💊 Extracted Drug List: {recommended}")

        # ✅ 복용 중 성분과 중복 제거
        filtered = filter_duplicate_ingredients(recommended, current_drugs)
        print(f"🧼 After Filtering: {filtered}")
        return filtered

    except Exception as e:
        print(f"❌ GPT 호출 실패: {e}")
        return []
