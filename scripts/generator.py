"""
레슨 생성 파이프라인 — 비개발자를 위한 교육 콘텐츠.

[설계 → 집필 → 코드 게이트 → 용어 게이트]

이전 설계(정보성 요약)와 결정적으로 다른 점은 '진실 기준'입니다.
요약글은 "소스에 있는가"가 기준이었지만, 설명글은 그게 의미가 없습니다.
대신 초보자에게 치명적인 두 가지를 기계로 막습니다.

    1. 예시 코드가 안 돌아간다  → code_runner
    2. 모르는 단어를 그냥 던진다 → jargon

두 게이트는 실패 시 모델에게 문제를 돌려주고 고치게 합니다. 그래도 안 되면
발행을 보류합니다. 나쁜 글을 안 쓰는 것이 이 파이프라인의 정상 동작입니다.

소스(웹 크롤)는 선택적 참고 자료입니다. '변수란 무엇인가'에 웹 소스가
필요하지는 않습니다. 다만 도구 이름·명령어·요금처럼 틀리면 독자가 따라 하다
막히는 사실은 소스에서 확인합니다.
"""

from google import genai
from api_utils import gemini_retry, gemini_limiter, gemini_tracker
import models
import code_runner
import jargon as jargon_gate

import os
import re
import sys
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

MAX_CODE_FIX_ROUNDS = 2
MAX_JARGON_FIX_ROUNDS = 1

STACK_LABEL = {
    "none": "코드 예시 없음 (개념 설명)",
    "python": "Python",
    "web": "HTML/CSS/JavaScript",
    "shell": "터미널 명령",
}


class LessonPlan(BaseModel):
    why_it_matters: str = Field(description="비개발자가 이걸 왜 알아야 하는지. 겪게 되는 상황으로 설명")
    analogy: str = Field(description="일상 경험에 빗댄 비유 한 가지")
    sections: List[str] = Field(description="설명 순서. 각 항목은 소제목이 될 문장")
    common_mistakes: List[str] = Field(description="초보자가 여기서 자주 막히는 지점 2~4개")
    check_yourself: str = Field(description="제대로 이해했는지 독자가 스스로 확인하는 방법")


class LessonDraft(BaseModel):
    title: str = Field(description="레슨 제목. 무엇을 알게 되는지 그대로 드러낼 것")
    content: str = Field(description="마크다운 본문")


def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY not found in .env")
        return None
    return genai.Client(api_key=key)


def _abort(reason, ctx=None):
    print(f"\n🛑 [ABORT] {reason}")
    print("   → 발행하지 않고 중단합니다.")
    return None, {"aborted": True, "reason": reason, "lesson_id": (ctx or {}).get("lesson_id"),
                  "source_text": ""}


def _strip_fence(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _context_block(ctx, sources_text):
    prereq = "\n".join(f"- [{p['title']}]({p['href']})" for p in ctx["prerequisites"]) or "- 없음 (이 블로그의 시작점입니다)"
    known = ", ".join(ctx["known_terms"]) or "(아직 없음 — 독자는 아무것도 모른다고 가정하라)"
    teaches = ", ".join(ctx["teaches"]) or "(지정 없음)"

    src = ""
    if sources_text:
        src = f"""
[참고 자료 — 도구 이름·명령어·요금처럼 '틀리면 독자가 막히는 사실'은 여기서 확인하라]
{sources_text[:20000]}
"""

    return f"""
[이번 레슨의 목표 — 독자가 읽고 나면 할 수 있어야 하는 것]
{ctx['goal']}

[트랙] {ctx['track_name']}
[예시 코드 언어] {STACK_LABEL.get(ctx['stack'], ctx['stack'])}

[먼저 읽고 온 글 — 여기 있는 내용은 다시 설명하지 말고, 필요하면 링크로 넘겨라]
{prereq}

[독자가 이미 배운 용어 — 다시 풀어쓸 필요 없다]
{known}

[이번 레슨에서 처음 설명할 용어 — 반드시 이 글 안에서 풀어써라]
{teaches}
{src}"""


def plan_lesson(client, ctx, sources_text):
    print("📝 [1/3] 레슨 설계: 무엇을 어떤 순서로 설명할지 정하는 중...")

    prompt = f"""
너는 비개발자에게 기술을 가르치는 선생이다. 아래 레슨의 설명 계획을 세워라.

독자는 개발자가 아니다. 코딩을 배운 적이 없고, 전문용어를 모른다.
AI로 뭔가 만들어보려다 막혀서 여기까지 온 사람이다.
{_context_block(ctx, sources_text)}

[계획 규칙]
1. why_it_matters 는 '언제 이것 때문에 막히는가'로 써라. 추상적인 중요성이 아니라 겪는 상황으로.
   - 나쁜 예: "터미널은 개발의 기본입니다"
   - 좋은 예: "AI가 '터미널에서 이 명령을 실행하세요'라고 답했을 때 어디에 쳐야 할지 몰라 멈추게 됩니다"
2. analogy 는 개발과 무관한 일상 경험에 빗대라. 비유가 억지스러우면 차라리 넣지 마라.
3. sections 는 3~5개. 목표에 도달하는 최단 경로여야 한다. 곁가지를 넣지 마라.
4. common_mistakes 는 실제로 초보자가 막히는 지점이어야 한다.
5. check_yourself 는 독자가 직접 해보고 확인할 수 있는 구체적 행동으로 써라.
"""

    @gemini_retry
    def call():
        gemini_limiter.consume()
        return client.models.generate_content(
            model=models.MAIN, contents=prompt,
            config={'response_mime_type': 'application/json', 'response_schema': LessonPlan})

    resp = call()
    gemini_tracker.add_text_usage(resp)
    plan = json.loads(resp.text)
    print(f"  ✅ 섹션 {len(plan.get('sections', []))}개 / 흔한 실수 {len(plan.get('common_mistakes', []))}개")
    return plan


def write_lesson(client, ctx, plan, sources_text):
    print("✍️ [2/3] 집필 중...")

    stack = ctx["stack"]
    if stack == "none":
        code_rule = """
[코드]
- 이 레슨은 개념 설명이다. 예시 코드를 억지로 넣지 마라.
- 파일 이름이나 화면에 보이는 텍스트를 인용할 때만 인라인 코드(`이렇게`)를 써라.
"""
    else:
        lang_tag = {"python": "python", "web": "html 또는 javascript", "shell": "bash"}[stack]
        code_rule = f"""
[코드 — 반드시 지켜라. 발행 전에 실제로 실행해서 검사한다]
- 코드블록에는 **반드시 언어 태그**를 붙여라: ```{lang_tag}
- 예시는 **그 자체로 완결되어 실행되는 것**이어야 한다. 조각만 보여주지 마라.
  독자는 그대로 복사해서 붙여넣는다. 앞뒤 맥락이 있어야 돌아가는 코드는 실패한다.
- 외부 라이브러리 설치나 API 키가 필요한 코드는 넣지 마라. 표준 기능만 써라.
- 일부러 틀린 예를 보여줄 때는 첫 줄에 이렇게 표시하라:
      # 잘못된 예 — 실행하면 오류가 납니다
  표시한 코드는 실제로 오류가 나야 한다. 멀쩡히 돌아가면 안 된다.
- 실행할 수 없는 예시(키 필요 등)는 첫 줄에 `# 실행 생략 — 이유` 를 적어라.
- **위험한 명령을 절대 싣지 마라**: sudo, rm -rf, chmod 777, curl | sh,
  git reset --hard, git push -f 등. 독자가 그대로 붙여넣는다.
- 코드를 보여준 뒤에는 **무엇이 일어나는지 한 줄씩 풀어써라.** 코드만 던지지 마라.
"""

    prompt = f"""
너는 '비개발노트'의 필자다. 개발자가 아니면서 먼저 배운 사람의 입장에서,
다음 사람이 같은 곳에서 막히지 않도록 설명하는 글을 쓴다.
{_context_block(ctx, sources_text)}

[설계안]
왜 알아야 하는가: {plan['why_it_matters']}
비유: {plan['analogy']}
설명 순서: {' / '.join(plan['sections'])}
흔히 막히는 지점: {' / '.join(plan['common_mistakes'])}
스스로 확인하기: {plan['check_yourself']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[집필 규칙]

1. 첫 문단
   - 이 글을 읽고 나면 무엇을 할 수 있게 되는지 먼저 말하라.
   - 그다음 '언제 이것 때문에 막히는지'를 한두 문장으로 붙여라.
   - "이번 시간에는 ~에 대해 알아보겠습니다" 같은 상투적 도입 금지.

2. 용어 — 이 규칙을 어기면 글이 반려된다
   - 위 [독자가 이미 배운 용어]에 없는 전문용어를 설명 없이 쓰지 마라.
   - 처음 쓸 때 그 자리에서 풀어써라. 괄호 풀이가 가장 자연스럽다.
     예: "터미널(명령어를 글자로 입력하는 검은 창)에서"
   - 영문 약어도 마찬가지다. API, CLI, DNS 전부 처음엔 풀어써라.
   - 먼저 읽고 온 글에서 다룬 내용은 다시 설명하지 말고 링크로 넘겨라.

3. 톤
   - '~습니다' 체. 아는 사람이 옆에서 차분히 알려주는 톤.
   - 독자를 낮잡아보지 마라. "쉽죠?", "간단합니다" 같은 말은 막힌 사람에게 상처가 된다.
   - 겪어보지 않은 경험을 지어내지 마라. "제가 3년간 써보니" 같은 문장 금지.
     "찾아보니", "저도 처음엔 헷갈렸습니다" 정도는 괜찮다.
   - 한 문단 2~4문장. 모바일에서 읽힌다.

4. 구조
   - 섹션 제목은 H2(`## `)로 시작하라. 본문에 H1을 쓰지 마라.
   - H3는 H2 안에서 더 쪼갤 내용이 있을 때만. 레벨을 건너뛰지 마라.
   - 마지막에 '흔히 막히는 지점'과 '스스로 확인하기'를 반드시 넣어라.
{code_rule}
5. 도해 — 구조가 있는 내용에만, 0~2개
   [도해: flow  | 단계1 > 단계2 > 단계3]        순서·절차
   [도해: stack | 상위 > 중간 > 하위]           계층·구성
   [도해: cycle | 단계1 > 단계2 > 단계3]        반복되는 주기
   각 항목에 `::` 로 짧은 설명을 붙일 수 있다. 항목 2~6개.
   구조화할 내용이 없으면 넣지 마라.

6. 분량
   - 하한선은 없다. 목표에 도달하면 거기서 끝내라.
   - 분량을 채우려고 일반론을 덧붙이지 마라.

7. 출력
   - FAQ 는 별도 시스템이 만든다. 본문에 쓰지 마라.
   - 제목과 본문만 출력하라. 프론트매터를 쓰지 마라.
"""

    @gemini_retry
    def call():
        gemini_limiter.consume()
        return client.models.generate_content(
            model=models.MAIN, contents=prompt,
            config={'response_mime_type': 'application/json', 'response_schema': LessonDraft})

    resp = call()
    gemini_tracker.add_text_usage(resp)
    data = json.loads(resp.text)
    data['content'] = _repair_layout(client, data.get('content', ''))
    print(f"  ✅ 초고: {data.get('title', '')}")
    return data


def fix_code(client, content, problems):
    """실행에 실패한 코드블록을 고치게 합니다."""
    prompt = f"""
아래 원고의 코드 예시에 문제가 있다. 코드만 고쳐서 원고 전문을 다시 내놓아라.

[발견된 문제]
{code_runner.format_problems(problems)}

[원고]
{content}

[수정 규칙]
1. 문제가 지적된 코드블록만 고쳐라. 다른 문장은 한 글자도 바꾸지 마라.
2. 예시는 그 자체로 완결되어 실행되어야 한다. 외부 라이브러리·API 키를 요구하지 마라.
3. 언어 태그가 없다는 지적이면 알맞은 태그를 붙여라.
4. 위험한 명령이라는 지적이면 그 명령을 안전한 것으로 바꾸거나 삭제하라.
5. '잘못된 예인데 정상 실행됨' 지적이면, 실제로 오류가 나는 코드로 바꾸거나 표시를 지워라.
6. 코드를 고쳤으면 그 아래 설명도 어긋나지 않게 맞춰라.
7. 원고 전문만 출력하라. 설명이나 코드펜스로 감싸지 마라.
"""

    @gemini_retry
    def call():
        gemini_limiter.consume()
        return client.models.generate_content(model=models.MAIN, contents=prompt)

    resp = call()
    gemini_tracker.add_text_usage(resp)
    return _strip_fence(resp.text)


def fix_jargon(client, content, undefined, ctx):
    """설명 없이 등장한 용어에 풀이를 넣게 합니다."""
    prompt = f"""
아래 원고에 비개발자가 모를 단어가 설명 없이 등장한다. 그 자리에 풀이를 넣어라.

[설명 없이 등장한 용어]
{jargon_gate.format_problems(undefined)}

[독자가 이미 배운 용어 — 이건 풀어쓸 필요 없다]
{', '.join(ctx['known_terms']) or '(없음)'}

[원고]
{content}

[수정 규칙]
1. 각 용어가 **처음 등장하는 자리**에 짧은 풀이를 넣어라. 괄호 풀이가 자연스럽다.
   예: "JSON(데이터를 주고받을 때 쓰는 글자 형식)"
2. 풀이는 그 자체로 또 다른 전문용어를 쓰면 안 된다.
3. 용어를 아예 빼도 뜻이 통하면 빼는 편이 낫다.
4. 지적되지 않은 문장은 건드리지 마라. 코드블록도 그대로 두어라.
5. 원고 전문만 출력하라. 설명이나 코드펜스로 감싸지 마라.
"""

    @gemini_retry
    def call():
        gemini_limiter.consume()
        return client.models.generate_content(model=models.MAIN, contents=prompt)

    resp = call()
    gemini_tracker.add_text_usage(resp)
    return _strip_fence(resp.text)


def generate_lesson(ctx, sources_text=""):
    """
    Args:
        ctx: teacher.next_lesson() 이 돌려준 컨텍스트
        sources_text: 선택적 참고 자료 (없어도 됨)

    Returns:
        (data, info) — data 가 None 이면 발행하지 않습니다.
    """
    client = _client()
    if client is None:
        return _abort("GEMINI_API_KEY 없음", ctx)

    print(f"\n🎓 레슨: {ctx['lesson_id']}  ({ctx['track_name']} · 진도 {ctx['progress']})")
    print(f"   목표: {ctx['goal']}")

    try:
        plan = plan_lesson(client, ctx, sources_text)
    except Exception as e:
        return _abort(f"레슨 설계 실패: {e}", ctx)

    try:
        draft = write_lesson(client, ctx, plan, sources_text)
    except Exception as e:
        return _abort(f"집필 실패: {e}", ctx)

    content = draft.get("content", "")
    if not content.strip():
        return _abort("집필 결과가 비어 있음", ctx)

    # ── 게이트 1: 예시 코드가 실제로 돌아가는가 ──────────────────────
    print("🧪 [3/3] 코드 게이트: 예시를 실제로 실행하는 중...")
    code_report = code_runner.check(content)
    print(f"  · {code_report['summary']}")
    rounds = 0
    while not code_report["ok"] and rounds < MAX_CODE_FIX_ROUNDS:
        rounds += 1
        for p in code_report["problems"][:5]:
            print(f"    ✗ [{p['block']}] {p['lang']}: {p['reason']}")
        print(f"  🔧 코드 수정 요청 ({rounds}/{MAX_CODE_FIX_ROUNDS})...")
        try:
            fixed = fix_code(client, content, code_report["problems"])
        except Exception as e:
            print(f"  ⚠️ 코드 수정 실패: {e}")
            break
        if len(fixed) < len(content) * 0.5:
            print("  ⚠️ 수정 결과가 과도하게 짧아 원본을 유지합니다.")
            break
        content = fixed
        code_report = code_runner.check(content)
        print(f"  · {code_report['summary']}")

    if not code_report["ok"]:
        for p in code_report["problems"][:5]:
            print(f"    ✗ [{p['block']}] {p['lang']}: {p['reason']} — {p['detail'][:100]}")
        return _abort(
            f"예시 코드 문제 {len(code_report['problems'])}건을 해결하지 못했습니다. "
            f"안 돌아가는 코드는 초보자를 좌절시킵니다.", ctx)

    print("  ✅ 코드 게이트 통과")

    # ── 게이트 2: 모르는 단어를 던지지 않았는가 ─────────────────────
    jr = jargon_gate.check(content, teaches=ctx["teaches"], known_terms=ctx["known_terms"])
    print(f"  · 용어 게이트: {jr['summary']}")
    rounds = 0
    while not jr["ok"] and rounds < MAX_JARGON_FIX_ROUNDS:
        rounds += 1
        for u in jr["undefined"][:6]:
            print(f"    ✗ {u['term']}")
        print(f"  🔧 용어 풀이 추가 요청 ({rounds}/{MAX_JARGON_FIX_ROUNDS})...")
        try:
            fixed = fix_jargon(client, content, jr["undefined"], ctx)
        except Exception as e:
            print(f"  ⚠️ 용어 수정 실패: {e}")
            break
        if len(fixed) < len(content) * 0.5:
            print("  ⚠️ 수정 결과가 과도하게 짧아 원본을 유지합니다.")
            break
        content = fixed
        # 코드가 망가지지 않았는지 다시 확인합니다.
        recheck = code_runner.check(content)
        if not recheck["ok"]:
            print("  ⚠️ 용어 수정 중 코드가 깨졌습니다. 용어 수정을 되돌립니다.")
            break
        jr = jargon_gate.check(content, teaches=ctx["teaches"], known_terms=ctx["known_terms"])
        print(f"  · 용어 게이트: {jr['summary']}")

    jargon_warning = None
    if not jr["ok"]:
        # 용어는 코드와 달리 발행을 막지는 않되, 보류 표시로 남깁니다.
        jargon_warning = f"설명 없이 등장한 용어 {len(jr['undefined'])}개: " + \
                         ", ".join(u["term"] for u in jr["undefined"][:8])
        print(f"  ⚠️ {jargon_warning}")
    else:
        print("  ✅ 용어 게이트 통과")

    draft["content"] = content
    return draft, {
        "aborted": False,
        "reason": None,
        "lesson_id": ctx["lesson_id"],
        "goal": ctx["goal"],
        "track": ctx["track"],
        "prerequisites": ctx["prerequisites"],
        "code_blocks": code_report["blocks"],
        "code_ran": code_report["ran"],
        "jargon_warning": jargon_warning,
        "source_text": sources_text,
    }


def _repair_layout(client, content):
    """구조화 출력이 줄바꿈을 잃어버리는 알려진 실패 모드를 복구합니다."""
    if '\\n' in content:
        print("  🔧 리터럴 '\\n' 감지 → 실제 줄바꿈으로 변환")
        content = content.replace('\\n', '\n')

    if content and content.count('\n') < 10:
        print("  🔧 줄바꿈 붕괴 감지 → 레이아웃 복원 시도")
        prompt = f"""You are a layout formatter. The input text has lost its paragraph breaks.
Re-insert proper newlines and restore a readable Markdown layout.

[UNFORMATTED TEXT]
{content}

[INSTRUCTIONS]
1. Output the fully formatted Markdown with proper newlines.
2. Put headings (##, ###), list items (-), code fences (```), images, and tables on their own lines.
3. Do not modify, rephrase, or translate a single word. Every word must be preserved.
4. Output ONLY the raw markdown. No code fences around the whole document, no explanation.
"""
        try:
            gemini_limiter.consume()
            resp = client.models.generate_content(model=models.FAST, contents=prompt)
            gemini_tracker.add_text_usage(resp)
            reconstructed = _strip_fence(resp.text)
            if len(reconstructed) > len(content) * 0.8:
                content = reconstructed
                print("  ✅ 레이아웃 복원 완료")
        except Exception as e:
            print(f"  ⚠️ 레이아웃 복원 실패: {e}")

    return content


# 이전 인터페이스 호환 (main.py 가 사용)
def generate_blog_post(crawled_content, folder="posts", additional_instructions="", keyword="",
                       schedule_type=None, question=None, reader=None, lesson_ctx=None):
    if lesson_ctx is None:
        return _abort("레슨 컨텍스트가 없습니다. teacher.next_lesson() 결과가 필요합니다.")
    sources = (crawled_content or {}).get("body", "") if crawled_content else ""
    return generate_lesson(lesson_ctx, sources_text=sources)


if __name__ == "__main__":
    import teacher
    cur = teacher.load_curriculum()
    lesson, ctx = teacher.next_lesson(cur)
    if lesson is None:
        print(ctx)
        raise SystemExit(0)
    data, info = generate_lesson(ctx)
    if data:
        print("\n=== TITLE ===\n" + data["title"])
        print("\n=== BODY (앞 1200자) ===\n" + data["content"][:1200])
    else:
        print(f"\nABORTED: {info['reason']}")
