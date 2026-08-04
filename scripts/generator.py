"""
정보성 콘텐츠 생성 파이프라인.

[구 설계 — 폐기]
  기획국장 → SEO/AEO/GEO 전문가 3인방 → 편집장
  · 전문가 3인방이 전부 기계(검색엔진)를 향해 최적화했고,
    "구체적 수치가 담긴 표를 반드시 생성하라"처럼 소스에 없는 사실을
    만들어내도록 지시하고 있었습니다.
  · 최종 집필 단계(편집장)가 원본 소스를 받지 못해 요약의 요약으로 글을 썼습니다.
  · "쓸 수 없음"이라는 결과가 없어서 소스가 부실해도 무조건 한 편을 뱉었습니다.

[신 설계]
  질문 정의 → 조사(근거 추출) → 집필
  · 명사 키워드가 아니라 '답할 수 있는 질문'에서 출발합니다.
    질문이 구체적이면 답의 범위가 정해지고 분량이 자동으로 결정됩니다.
  · 조사 단계는 소스에서 근거 문장을 그대로 뽑아옵니다. 답이 없으면 없다고 보고합니다.
  · 근거가 부족하면 ABORT 합니다. 나쁜 글을 안 쓰는 것이 품질의 대부분입니다.
  · 집필 단계는 원본 소스와 조사 결과를 모두 받습니다.

검색엔진 최적화(canonical / hreflang / JSON-LD / OG / sitemap)는
src/layouts/Layout.astro 와 PostDetails.astro 가 이미 전부 처리합니다.
글 쓰는 프롬프트에서 SEO를 할 이유가 없습니다.
"""

from google import genai
from api_utils import gemini_retry, gemini_limiter, gemini_tracker
import models
import os
import re
from dotenv import load_dotenv
import json
from pydantic import BaseModel, Field
from typing import List

import sys

load_dotenv()

if sys.platform == "win32":
    # Ensure terminal can handle UTF-8/Emojis on Windows
    sys.stdout.reconfigure(encoding='utf-8')


# ── 조사 결과가 이 기준에 못 미치면 글을 쓰지 않습니다 ──────────────────
MIN_CONFIRMED_FINDINGS = 3      # 소스로 확인된 답이 최소 3개
MIN_COVERAGE = 0.5              # 하위 질문의 절반 이상이 답변되어야 함


class QuestionFrame(BaseModel):
    main_question: str = Field(description="독자가 실제로 검색할 법한, 답할 수 있는 구체적인 질문 1개")
    reader: str = Field(description="이 질문을 검색하는 사람이 처한 상황 한 문장")
    sub_questions: List[str] = Field(description="본문을 답하려면 먼저 해결해야 할 하위 질문 3~6개")


class Finding(BaseModel):
    sub_question: str = Field(description="어떤 하위 질문에 대한 답인지")
    answer: str = Field(description="소스에 근거한 답. 소스에 없으면 비워 둘 것")
    evidence: str = Field(description="근거가 된 소스 원문 구절을 그대로 발췌. 요약·의역 금지")
    source_url: str = Field(description="근거가 나온 출처 URL")
    status: str = Field(description="confirmed | partial | not_found 중 하나")


class ResearchOutput(BaseModel):
    findings: List[Finding] = Field(description="하위 질문별 조사 결과")
    conflicts: List[str] = Field(description="소스끼리 서로 다르게 말하는 지점. 없으면 빈 배열")
    unanswered: List[str] = Field(description="주어진 소스로는 답할 수 없는 하위 질문. 없으면 빈 배열")


class BlogPostSchema(BaseModel):
    title: str = Field(description="최종 완성된 제목")
    content: str = Field(description="마크다운 형식의 최종 완성된 본문")


def _client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None
    return genai.Client(api_key=api_key)


def _abort(reason, question=None):
    print(f"\n🛑 [ABORT] {reason}")
    print("   → 발행하지 않고 중단합니다. (나쁜 글을 쓰지 않는 것이 이 파이프라인의 정상 동작입니다)")
    return None, {
        "aborted": True,
        "reason": reason,
        "question": question,
        "coverage": 0.0,
        "conflicts": [],
        "unanswered": [],
        "source_text": "",
    }


def generate_informational_post(crawled_content, keyword="", schedule_type=None):
    """
    질문 정의 → 조사 → 집필.

    Returns:
        (data, info)
        data: {"title": ..., "content": ...} 또는 None(중단 시)
        info: 중단 사유 / 커버리지 / 상충 목록 / 원본 소스 텍스트
    """
    client = _client()
    if client is None:
        return _abort("GEMINI_API_KEY 없음")

    primary_topic = keyword if keyword else crawled_content['title']
    source_text = crawled_content['body']

    data_block = f"""
### 주제:
{primary_topic}

### 수집된 소스 (원문):
출처 URL: {crawled_content['url']}
본문:
{source_text}
"""

    # ── PHASE 1: 질문 정의 ────────────────────────────────────────────
    print(f"\n❓ [1/3] 질문 정의: 답할 수 있는 형태로 주제를 좁히는 중... (Schedule: {schedule_type or 'Manual'})")

    framing_prompt = f"""
너는 기술 문서의 '질문 정의자'다. 블로그 주제로 던져진 명사형 키워드를,
독자가 실제로 검색하고 답을 얻어갈 수 있는 '구체적인 질문'으로 바꾸는 것이 임무다.

{data_block}

[규칙]
1. main_question 은 반드시 물음표로 끝나는 하나의 질문이어야 한다.
   - 나쁜 예: "멀티모달 AI" (명사. 범위가 무한해서 답할 수 없다)
   - 좋은 예: "사내 문서 검색에 멀티모달 모델을 쓰면 텍스트 전용 대비 무엇이 달라지나?"
2. 질문은 **주어진 소스로 답할 수 있는 범위** 안에서 만들어라.
   소스에 없는 내용을 묻는 질문을 만들면 안 된다.
3. sub_questions 는 main_question 에 답하기 위해 순서대로 해결해야 할 것들이다.
   개념 정의 → 동작 방식 → 선택 기준 → 주의점 순으로 자연스럽게 이어지게 하라.
4. 논쟁적 제목("혁신인가 함정인가", "~의 역설")을 만들지 마라.
   이 블로그는 의견 칼럼이 아니라 정보성 문서다.
"""

    @gemini_retry
    def call_framer():
        gemini_limiter.consume()
        return client.models.generate_content(
            model=models.MAIN,
            contents=framing_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': QuestionFrame}
        )

    try:
        frame_resp = call_framer()
        gemini_tracker.add_text_usage(frame_resp)
        frame = json.loads(frame_resp.text)
    except Exception as e:
        return _abort(f"질문 정의 실패: {e}")

    main_question = frame.get("main_question", "").strip()
    sub_questions = [q for q in frame.get("sub_questions", []) if q and q.strip()]

    if not main_question or not sub_questions:
        return _abort("질문 정의 결과가 비어 있음")

    print(f"  ✅ 질문: {main_question}")
    print(f"     하위 질문 {len(sub_questions)}개 / 독자: {frame.get('reader', '')[:60]}")

    # ── PHASE 2: 조사 ────────────────────────────────────────────────
    print("🔎 [2/3] 조사: 소스에서 근거를 추출하는 중...")

    research_prompt = f"""
너는 기술 문서의 '조사원'이다. 아래 소스만을 근거로 하위 질문들에 답하라.
너는 글을 쓰지 않는다. 근거를 수집해서 보고하는 역할이다.

[답해야 할 질문]
{main_question}

[하위 질문]
{chr(10).join(f"- {q}" for q in sub_questions)}

{data_block}

[절대 규칙]
1. **소스에 없는 내용은 절대 만들지 마라.** 배경지식으로 아는 것도 쓰지 마라.
   소스에 답이 없으면 status 를 "not_found" 로 하고 answer 를 비워라.
   답이 없다고 보고하는 것은 실패가 아니라 정상적인 결과다.
2. evidence 에는 소스 원문의 구절을 **글자 그대로** 발췌하라. 요약하거나 다듬지 마라.
   evidence 를 채울 수 없으면 그 답은 confirmed 가 아니다.
3. 수치(연도, 퍼센트, 배수, 용량, 가격 등)는 소스에 그 숫자가 실제로 적혀 있을 때만 answer 에 포함하라.
   "약 5Gbps 수준" 처럼 소스에 없는 값을 추정해서 쓰는 것을 금지한다.
4. 소스들이 서로 다르게 말하는 지점이 있으면 감추지 말고 conflicts 에 적어라.
   ("A 문서는 X라 하고 B 문서는 Y라 한다" 형식)
5. status 는 셋 중 하나다.
   - confirmed: 소스에 명확한 답이 있고 evidence 를 그대로 인용할 수 있다
   - partial: 부분적으로만 답할 수 있다
   - not_found: 소스로는 답할 수 없다
"""

    @gemini_retry
    def call_researcher():
        gemini_limiter.consume()
        return client.models.generate_content(
            model=models.MAIN,
            contents=research_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': ResearchOutput}
        )

    try:
        research_resp = call_researcher()
        gemini_tracker.add_text_usage(research_resp)
        research = json.loads(research_resp.text)
    except Exception as e:
        return _abort(f"조사 단계 실패: {e}", main_question)

    findings = research.get("findings", []) or []
    conflicts = research.get("conflicts", []) or []
    unanswered = research.get("unanswered", []) or []

    confirmed = [f for f in findings if f.get("status") == "confirmed" and f.get("evidence", "").strip()]
    partial = [f for f in findings if f.get("status") == "partial"]
    coverage = len(confirmed) / len(sub_questions) if sub_questions else 0.0

    print(f"  · 확인됨 {len(confirmed)} / 부분 {len(partial)} / 미답변 {len(unanswered)}")
    print(f"  · 커버리지 {coverage*100:.0f}% (기준 {MIN_COVERAGE*100:.0f}%)")
    if conflicts:
        print(f"  · 소스 간 상충 {len(conflicts)}건 — 본문에 명시합니다")

    # ── 중단 게이트 ───────────────────────────────────────────────────
    if len(confirmed) < MIN_CONFIRMED_FINDINGS:
        return _abort(
            f"소스로 확인된 답이 {len(confirmed)}개뿐입니다 (최소 {MIN_CONFIRMED_FINDINGS}개 필요). "
            f"이 주제는 지금 가진 소스로 쓸 수 없습니다.",
            main_question,
        )

    if coverage < MIN_COVERAGE:
        return _abort(
            f"하위 질문 커버리지 {coverage*100:.0f}% (기준 {MIN_COVERAGE*100:.0f}%). "
            f"질문의 절반도 답하지 못한 글은 독자에게 쓸모가 없습니다.",
            main_question,
        )

    # ── PHASE 3: 집필 ────────────────────────────────────────────────
    print("✍️ [3/3] 집필: 조사 결과로 답변 문서를 작성하는 중...")

    evidence_block = "\n\n".join(
        f"[하위 질문] {f.get('sub_question','')}\n"
        f"[답] {f.get('answer','')}\n"
        f"[근거 원문] {f.get('evidence','')}\n"
        f"[출처] {f.get('source_url','')}"
        for f in (confirmed + partial)
    )

    conflict_block = ""
    if conflicts:
        conflict_block = (
            "\n[소스 간 상충 — 숨기지 말고 본문에 그대로 드러내라]\n"
            + "\n".join(f"- {c}" for c in conflicts)
        )

    unanswered_block = ""
    if unanswered:
        unanswered_block = (
            "\n[소스로 답할 수 없었던 질문 — 아는 척하지 말고 아예 다루지 마라]\n"
            + "\n".join(f"- {q}" for q in unanswered)
        )

    writer_prompt = f"""
너는 기술 문서 집필자다. 아래 질문에 답하는 문서를 쓴다.
의견 칼럼이 아니다. 논조도, 주장도, 반전도 필요 없다.
독자는 답을 찾으러 왔고, 답을 얻으면 떠난다. 그것으로 충분하다.

[답해야 할 질문]
{main_question}

[독자]
{frame.get('reader', '')}

[조사원이 소스에서 확인한 내용 — 이것만 쓸 수 있다]
{evidence_block}
{conflict_block}
{unanswered_block}

[원본 소스 — 문맥 확인용. 여기 없는 사실은 쓸 수 없다]
{source_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[집필 규칙]

1. 사실의 출처
   - 위 조사 결과와 원본 소스에 있는 내용만 써라.
   - 수치·버전·제품명·API 이름·기관명은 소스에 그대로 등장할 때만 써라.
     소스에 없는 값을 추정하거나 반올림해서 쓰지 마라.
   - 소스가 답하지 못한 부분은 그냥 다루지 마라. 추측으로 메우지 마라.

2. 구조는 질문에서 나온다
   - 목차를 미리 정해두고 채우지 마라. "이 질문에 답하려면 무엇을 먼저 설명해야 하는가"로 결정하라.
   - 첫 두세 문장 안에 질문에 대한 **직접적인 답**을 먼저 제시하라.
     독자가 스크롤을 내려야 답을 만나게 하지 마라.
   - 🚨 **섹션 제목은 반드시 H2(`## `)로 시작하라.** 본문 최상위 섹션에 H3(`### `)를 쓰면 안 된다.
     제목(H1)은 시스템이 따로 붙이므로 본문에 H1을 쓰지 마라.
     H3(`### `)는 H2 섹션 안에서 더 쪼갤 내용이 있을 때만 쓴다. 레벨을 건너뛰면 안 된다.
   - 빈 소제목을 만들지 마라. 소제목 아래에는 반드시 문장이 와야 한다.

3. 표
   - 비교할 대상이 실제로 둘 이상이고, 각 칸을 소스 근거로 채울 수 있을 때만 만들어라.
   - 칸을 채우려고 값을 지어내야 한다면 표를 만들지 마라. 표는 필수가 아니다.

4. 금지
   - 큰따옴표로 감싼 인용문을 만들지 마라. 실명 화자가 없는 인용은 독자를 오도한다.
   - "결론적으로", "요약하자면", "급변하는 IT 환경 속에서", "~에 대해 알아보겠습니다" 금지.
   - "혁신적인", "치명적인", "전례 없는", "완벽한" 같은 과장 형용사 금지.
   - 스스로를 "필자는", "전문가로서" 라고 지칭하지 마라.
   - 굵은 글씨를 남발하지 마라. 한 섹션에 1~2회면 충분하다.

5. 분량
   - **하한선은 없다.** 질문에 답이 끝나면 거기서 끝내라.
   - 분량을 채우려고 같은 말을 바꿔 쓰거나 일반론을 덧붙이는 것을 금지한다.

6. 톤
   - 아는 사람이 옆에서 차분히 설명해주는 톤. '~습니다' 체.
   - 한 문단 2~4문장. 모바일에서 읽힌다는 것을 기억하라.

7. 도해
   - 분위기용 삽화는 넣지 마라. 정보성 문서에서 장식 이미지는 독자가 답을 찾는 데 도움이 되지 않는다.
   - 단계·계층·주기처럼 **구조가 있는 내용을 설명할 때만** 아래 표기를 쓴다. 0~2개.
     [도해: flow  | 단계1 > 단계2 > 단계3]           ← 순서·절차
     [도해: stack | 상위계층 > 중간계층 > 하위계층]   ← 계층·구성
     [도해: cycle | 단계1 > 단계2 > 단계3]           ← 반복되는 주기
   - 항목은 2~6개. 각 항목에 `::` 로 짧은 설명을 붙일 수 있다.
     예: [도해: flow | 실험::모델·프롬프트 비교 > 배포::API 레이어 구성 > 모니터링]
   - 항목 이름은 **본문에 실제로 등장한 표현**을 그대로 써라. 도해용으로 새 개념을 만들지 마라.
   - 구조화할 내용이 없으면 도해를 넣지 마라. 억지로 만들지 마라.

8. 출력
   - FAQ 섹션은 별도 시스템이 생성하므로 본문에 쓰지 마라.
   - 제목과 본문만 출력하라. 프론트매터는 쓰지 마라.
"""

    @gemini_retry
    def call_writer():
        gemini_limiter.consume()
        return client.models.generate_content(
            model=models.MAIN,
            contents=writer_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': BlogPostSchema}
        )

    try:
        final_resp = call_writer()
        gemini_tracker.add_text_usage(final_resp)
        final_data = json.loads(final_resp.text)
    except Exception as e:
        return _abort(f"집필 단계 실패: {e}", main_question)

    content = _repair_layout(client, final_data.get('content', ''))
    if not content.strip():
        return _abort("집필 결과가 비어 있음", main_question)

    final_data['content'] = content
    print(f"  ✅ 초고 완성: {final_data.get('title','')}")

    return final_data, {
        "aborted": False,
        "reason": None,
        "question": main_question,
        "coverage": coverage,
        "conflicts": conflicts,
        "unanswered": unanswered,
        "source_text": source_text,
    }


def _repair_layout(client, content):
    """
    구조화 출력이 줄바꿈을 잃어버리는 알려진 실패 모드를 복구합니다.
    (ERRORS.md 2026-05-11 항목 참조)
    """
    if '\\n' in content:
        print("  🔧 리터럴 '\\n' 감지 → 실제 줄바꿈으로 변환")
        content = content.replace('\\n', '\n')

    if content and content.count('\n') < 10:
        print("  🔧 줄바꿈 붕괴 감지 → 레이아웃 복원 시도")
        restore_prompt = f"""
You are a layout formatter. The input text has lost its paragraph breaks.
Re-insert proper newlines and restore a readable Markdown layout.

[UNFORMATTED TEXT]
{content}

[INSTRUCTIONS]
1. Output the fully formatted Markdown text with proper newlines.
2. Put headings (##, ###), list items (-), images (![), and tables (|) on their own lines.
3. Do not modify, rephrase, or translate a single word. Every word must be preserved.
4. Output ONLY the raw markdown content. No code fences, no explanation.
"""
        try:
            gemini_limiter.consume()
            resp = client.models.generate_content(model=models.FAST, contents=restore_prompt)
            gemini_tracker.add_text_usage(resp)
            reconstructed = resp.text.strip()
            if reconstructed.startswith("```"):
                lines = reconstructed.split("\n")
                if lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                reconstructed = "\n".join(lines).strip()
            if len(reconstructed) > len(content) * 0.8:
                content = reconstructed
                print("  ✅ 레이아웃 복원 완료")
            else:
                print("  ⚠️ 복원 결과가 너무 짧아 건너뜁니다")
        except Exception as e:
            print(f"  ⚠️ 레이아웃 복원 실패: {e}")

    return content


def generate_blog_post(crawled_content, folder="posts", additional_instructions="", keyword="", schedule_type=None):
    """
    진입점.

    용어사전(glossary) 경로는 폐지했습니다. 포스트 한 편마다 용어사전 한 편을
    자동 생성하던 구조 때문에 포스트 118편에 용어사전 109편이 쌓였고,
    콘텐츠의 절반이 자동 생성 사전 항목이 되어 있었습니다.

    Returns:
        (data, info) — data 가 None 이면 발행하지 않아야 합니다. info["reason"] 에 사유가 있습니다.
    """
    return generate_informational_post(crawled_content, keyword=keyword, schedule_type=schedule_type)


if __name__ == "__main__":
    dummy_content = {
        "title": "Astro v5 Released",
        "url": "https://astro.build/blog/v5-released/",
        "body": "Astro v5 is here with many new features and performance improvements. "
                "It includes new rendering modes and better SEO support.",
    }

    post, info = generate_blog_post(crawled_content=dummy_content, folder="posts", keyword="Astro v5")

    if post:
        print("=== GENERATED DRAFT ===")
        print(post['title'])
        print(post['content'][:500])
    else:
        print(f"=== ABORTED: {info['reason']} ===")
