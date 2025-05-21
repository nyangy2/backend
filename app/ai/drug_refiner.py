import openai
import re
from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

def refine_ocr_lines_with_gpt(lines: list[str]) -> list[str]:
    numbered_list = "\n".join([f"{i+1}. {line}" for i, line in enumerate(lines)])

    prompt = f"""
    다음은 OCR로 추출된 약품명 후보 텍스트입니다.
    이 중 일부는 약품명이 아닌 일반 단어나 안내 문구일 수 있습니다.

    각 항목에 대해:
    - 한국에서 실제 유통 중인 약품명과 **1~2글자 정도 오타가 있을 수 있습니다.**
    - 실제 존재하는 약품명과 비슷한 경우, 가능한 정확한 제품명으로 보정해주세요.
    - 오타, 숫자, 단위, 괄호 내용, 설명 문구는 제거하고 **짧고 정확한 제품명만** 출력해주세요.
    - 의약품이 아닌 일반 단어(예: 정보, 주의, 회 등)나 병원 문구는 **"제외"**라고 명시해주세요.

    약품명 후보 목록:
    {numbered_list}

    결과는 아래처럼 리스트 형식으로 주세요:
    1. 정제된약품명 또는 제외
    2. ...
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    refined_lines = []
    for line in content.splitlines():
        if match := re.match(r"\d+\.\s*(.+)", line):
            refined_lines.append(match.group(1).strip())

    return refined_lines
