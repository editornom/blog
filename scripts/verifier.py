"""
발행 관문 (Fact Gate).

원고에 적힌 사실 주장이 실제 소스에 존재하는지 대조합니다.
기존 파이프라인에는 이 단계가 아예 없었고, 그 결과 소스에 없는 벤치마크 수치와
API 기본값이 그대로 발행됐습니다.

2단 구성:
  1단 — 결정론적 대조 (모델 미개입)
        본문의 수치 주장을 뽑아 소스 원문에 문자열로 존재하는지 확인합니다.
        모델의 판단이 개입하지 않으므로 가장 신뢰할 수 있는 층입니다.
  2단 — 교정 (모델)
        1단에서 걸린 항목이 있으면, 그 문장을 소스 근거대로 고치거나 삭제하게 합니다.
        교정 후 다시 1단을 돌려서 남아 있으면 발행을 보류합니다.

판정:
  pass    — 미검증 수치 없음
  revised — 교정 후 통과
  hold    — 교정 후에도 미검증 수치가 남음 → draft:true 로 보류
"""

import os
import re
import json
from dotenv import load_dotenv

from google import genai
from api_utils import gemini_retry, gemini_limiter, gemini_tracker
import models

load_dotenv()

# 교정 후에도 이 개수를 넘게 남으면 발행 보류
MAX_UNVERIFIED_AFTER_FIX = 0


# 숫자 주장으로 볼 패턴. 목록 번호나 헤딩 번호 같은 잡음은 제외합니다.
_CLAIM_PATTERNS = [
    r'\d+(?:\.\d+)?\s*%',                                               # 퍼센트
    r'\d+(?:\.\d+)?\s*(?:GB|MB|TB|KB|PB|Gbps|Mbps|Kbps|GHz|MHz|ms|μs)', # 단위
    r'(?:19|20)\d{2}\s*년?',                                            # 연도
    r'\d+(?:\.\d+)?\s*(?:배|억|조|만|천만|백만)',                        # 배수·규모
    r'\d{1,3}(?:,\d{3})+',                                              # 천단위 구분 숫자
    r'\d{3,}',                                                          # 세 자리 이상 숫자
    r'v?\d+\.\d+(?:\.\d+)?',                                            # 버전
]

_CLAIM_RE = re.compile("|".join(f"(?:{p})" for p in _CLAIM_PATTERNS))


def _strip_noise(markdown: str) -> str:
    """검증 대상에서 제외할 영역을 제거합니다 (경로·URL·코드블록·번호매김에는 숫자가 많습니다)."""
    text = markdown
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)   # 프론트매터
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)          # 코드블록
    text = re.sub(r'`[^`]*`', ' ', text)                             # 인라인 코드
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', text)                # 이미지
    text = re.sub(r'\]\([^)]*\)', '] ', text)                        # 링크 경로
    text = re.sub(r'https?://\S+', ' ', text)                        # 맨 URL
    text = re.sub(r'<[^>]+>', ' ', text)                             # HTML 태그(툴팁 등)

    # 문서 번호매김은 사실 주장이 아닙니다.
    # "### 2.3. 제목" 의 2.3 을 버전 번호로 오인하면 모든 글이 보류 판정을 받습니다.
    text = re.sub(r'^\s*#{1,6}\s*\d+(?:\.\d+)*\.?\s*', '## ', text, flags=re.MULTILINE)  # 헤딩 번호
    text = re.sub(r'^\s*\d+(?:\.\d+)*\.\s+', '', text, flags=re.MULTILINE)               # 순서 목록
    return text


def _normalize(s: str) -> str:
    """공백과 천단위 쉼표를 제거해 표기 차이를 흡수합니다."""
    return re.sub(r'[\s,]', '', s)


def extract_claims(markdown: str):
    """본문에서 수치 주장 후보를 중복 없이 추출합니다."""
    text = _strip_noise(markdown)
    seen, claims = set(), []
    for m in _CLAIM_RE.finditer(text):
        raw = m.group(0).strip()
        key = _normalize(raw)
        if len(key) < 2 or key in seen:
            continue
        seen.add(key)
        # 문맥 한 줄을 같이 담아 교정 단계에서 쓰게 합니다.
        line_start = text.rfind('\n', 0, m.start()) + 1
        line_end = text.find('\n', m.end())
        line = text[line_start:line_end if line_end != -1 else len(text)].strip()
        claims.append({"claim": raw, "context": line[:300]})
    return claims


def check_claims(markdown: str, source_text: str):
    """소스에 존재하지 않는 수치 주장 목록을 돌려줍니다. 모델 미개입."""
    haystack = _normalize(source_text)
    unverified = []
    for c in extract_claims(markdown):
        if _normalize(c["claim"]) not in haystack:
            unverified.append(c)
    return unverified


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=api_key) if api_key else None


def _revise(markdown: str, source_text: str, unverified):
    """미검증 수치가 포함된 문장을 소스 근거대로 고치거나 삭제합니다."""
    client = _client()
    if client is None:
        return markdown

    items = "\n".join(
        f'- "{u["claim"]}"  (문장: {u["context"]})' for u in unverified[:30]
    )

    prompt = f"""
너는 사실 검증 편집자다. 아래 원고에는 출처를 확인할 수 없는 수치가 들어 있다.
이것들을 처리한 원고를 돌려주는 것이 임무다.

[출처를 확인할 수 없는 수치]
{items}

[원본 소스 — 유일하게 인정되는 근거]
{source_text}

[원고]
{markdown}

[처리 규칙]
1. 위 수치가 소스에 실제로 있으면 그대로 둔다.
2. 소스에 없으면 다음 중 하나로 처리한다.
   a. 소스에 있는 올바른 값으로 교체한다.
   b. 수치를 빼고 문장을 정성적으로 다시 쓴다. (예: "약 40% 빠르다" → "더 빠르다")
   c. 그 문장이 수치 없이는 의미가 없으면 문장 전체를 삭제한다.
3. **새로운 수치를 절대 추가하지 마라.** 이 단계는 수치를 줄이는 단계다.
4. 수치와 무관한 문장은 한 글자도 건드리지 마라. 문체 손질을 하지 마라.
5. 마크다운 구조(헤딩, 표, 이미지, 링크, 프론트매터)를 그대로 보존하라.
6. 교정된 원고 전문만 출력하라. 설명이나 코드펜스를 붙이지 마라.
"""

    @gemini_retry
    def call():
        gemini_limiter.consume()
        return client.models.generate_content(model=models.MAIN, contents=prompt)

    try:
        resp = call()
        gemini_tracker.add_text_usage(resp)
        revised = resp.text.strip()
        if revised.startswith("```"):
            lines = revised.split("\n")
            if lines[0].strip().startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            revised = "\n".join(lines).strip()
        # 안전장치: 교정 결과가 비정상적으로 짧으면 원본을 유지합니다.
        if len(revised) < len(markdown) * 0.5:
            print("  ⚠️ [Fact Gate] 교정 결과가 과도하게 짧아 원본을 유지합니다.")
            return markdown
        return revised
    except Exception as e:
        print(f"  ⚠️ [Fact Gate] 교정 실패: {e}")
        return markdown


def verify(markdown: str, source_text: str):
    """
    Returns:
        (content, verdict, report)
        verdict: "pass" | "revised" | "hold"
    """
    print("\n=== Fact Gate: 수치 주장 소스 대조 ===")

    if not source_text or not source_text.strip():
        print("  ⚠️ 소스 텍스트가 없어 검증을 건너뜁니다.")
        return markdown, "pass", {"before": [], "after": [], "skipped": True}

    before = check_claims(markdown, source_text)
    total = len(extract_claims(markdown))
    print(f"  · 수치 주장 {total}건 중 미검증 {len(before)}건")

    if not before:
        print("  ✅ 통과 — 모든 수치가 소스에서 확인됩니다.")
        return markdown, "pass", {"before": [], "after": [], "skipped": False}

    for u in before[:10]:
        print(f"    ✗ {u['claim']}  ←  {u['context'][:80]}")

    print("  🔧 미검증 수치 교정 중...")
    revised = _revise(markdown, source_text, before)
    after = check_claims(revised, source_text)

    print(f"  · 교정 후 미검증 {len(after)}건")

    if len(after) <= MAX_UNVERIFIED_AFTER_FIX:
        print("  ✅ 교정 후 통과")
        return revised, "revised", {"before": before, "after": after, "skipped": False}

    print(f"  🛑 미검증 수치가 {len(after)}건 남았습니다 → draft:true 로 보류합니다.")
    for u in after[:10]:
        print(f"    ✗ {u['claim']}  ←  {u['context'][:80]}")
    return revised, "hold", {"before": before, "after": after, "skipped": False}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("usage: python verifier.py <post.md> <source.txt>")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        md = f.read()
    with open(sys.argv[2], encoding="utf-8") as f:
        src = f.read()
    _, verdict, report = verify(md, src)
    print(json.dumps({"verdict": verdict, "unverified_after": report["after"]},
                     ensure_ascii=False, indent=2))
