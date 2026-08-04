"""
용어 게이트 — "비개발자가 읽을 수 있는가"를 기계적으로 검사합니다.

교육 콘텐츠가 실패하는 두 번째 방식은 설명 없이 전문용어를 던지는 것입니다.
글쓴이에게는 당연한 단어라 자기 눈에는 안 보입니다. 그래서 사람이 아니라
코드가 잡아야 합니다.

동작
  1. 커리큘럼의 teaches 를 모아 '이미 가르친 용어' 목록을 만듭니다 (teacher.py 제공)
  2. 본문에서 전문용어 후보를 찾습니다
     - 사전에 등록된 IT 용어
     - 영문 대문자 약어 (API, HTTP, CLI …)
     - 영문 단어가 한글 사이에 끼어 있는 경우
  3. 다음에 해당하면 통과
     - 이번 레슨이 가르치기로 한 용어(teaches)
     - 이전 레슨에서 이미 가르친 용어
     - 본문에서 첫 등장 직후에 설명이 붙어 있는 경우
       (괄호 풀이, '~란', '~는 ...입니다', 볼드 정의 등)
  4. 나머지는 '설명 없이 등장한 용어'로 보고합니다

코드블록 안은 검사하지 않습니다. 코드에 API 라고 적힌 건 설명 대상이 아닙니다.
"""

import re

# 설명 없이 던지면 비개발자가 막히는 용어들.
# 커리큘럼의 teaches 로 덮이지 않는 것들을 보완합니다.
JARGON = {
    "런타임", "컴파일", "빌드", "배포", "롤백", "마이그레이션", "리팩터링",
    "리포지토리", "저장소", "커밋", "브랜치", "머지", "풀리퀘스트", "클론",
    "디펜던시", "의존성", "패키지", "라이브러리", "프레임워크", "모듈",
    "엔드포인트", "페이로드", "파싱", "직렬화", "캐시", "캐싱",
    "비동기", "동기", "콜백", "프로미스", "스레드", "프로세스",
    "인스턴스", "객체", "클래스", "메서드", "속성", "상속",
    "쿼리", "스키마", "인덱스", "트랜잭션", "마이그레이션",
    "인증", "인가", "토큰", "세션", "쿠키", "해시", "암호화",
    "포트", "프로토콜", "헤더", "도메인", "서브도메인", "리다이렉트",
    "환경변수", "설정 파일", "로그", "디버깅", "예외", "스택 트레이스",
    "컨테이너", "이미지", "가상화", "인스턴스", "리전",
    "프론트엔드", "백엔드", "서버리스", "미들웨어", "라우팅",
    "터미널", "셸", "커맨드", "플래그", "옵션", "인자", "파라미터",
    "레포", "푸시", "풀", "스테이징", "체크아웃",
}

# 영문 약어 (2~6자 대문자). 코드 밖에서 쓰이면 설명이 필요합니다.
_ACRONYM = re.compile(r'\b([A-Z][A-Z0-9]{1,5})\b')

# 한글 사이에 낀 영문 단어
_EMBEDDED_EN = re.compile(r'[가-힣]\s*([A-Za-z][A-Za-z0-9.+-]{2,})\s*[가-힣]')

# 설명이 붙었다고 인정하는 형태
_DEFINED_PATTERNS = [
    r'{t}\s*\(([^)]{{4,}})\)',              # 용어(풀이)
    r'\(\s*{t}\s*\)',                        # 풀이(용어)
    r'{t}\s*(?:란|이란|는|은)\s+[^.\n]{{8,}}(?:입니다|말합니다|뜻입니다|의미합니다)',
    r'\*\*{t}\*\*\s*[:：-]',                 # **용어**: 설명
    r'{t}\s*[:：]\s*\S',                     # 용어: 설명
]

# 일상어가 되어 설명이 필요 없는 것들
ALLOWLIST = {
    "AI", "IT", "PC", "OS", "URL", "USB", "PDF", "SNS", "TV", "CPU", "RAM",
    "ID", "OK", "NO", "FAQ", "Q", "A", "KST", "UTC",
}


def _strip_code(markdown):
    """코드블록·인라인 코드·프론트매터·HTML 태그를 제거합니다."""
    t = re.sub(r'^---\n.*?\n---\n', '', markdown, flags=re.DOTALL)
    t = re.sub(r'```.*?```', ' ', t, flags=re.DOTALL)
    t = re.sub(r'`[^`]*`', ' ', t)
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'https?://\S+', ' ', t)
    return t


def _is_defined_near(text, term, first_pos):
    """첫 등장 주변에 설명이 붙어 있는지 확인합니다."""
    window = text[max(0, first_pos - 120): first_pos + 400]
    esc = re.escape(term)
    for pat in _DEFINED_PATTERNS:
        if re.search(pat.format(t=esc), window):
            return True
    return False


_HANGUL = re.compile(r'[가-힣]')

# 용어 뒤에 붙어도 같은 낱말로 보는 조사·어미. 이 밖의 한글이 이어지면
# 다른 낱말의 일부로 봅니다. ("프로그램"의 '로그', "로그인"의 '로그')
_PARTICLES = set("을를이가은는에의와과로도만나며서부까다요표")


def _is_standalone(text, term, start):
    """한국어 용어가 다른 낱말의 일부로 잡힌 것인지 판별합니다."""
    prev_ch = text[start - 1] if start > 0 else ""
    if _HANGUL.match(prev_ch or ""):
        return False
    end = start + len(term)
    next_ch = text[end] if end < len(text) else ""
    if next_ch and _HANGUL.match(next_ch) and next_ch not in _PARTICLES:
        return False
    return True


def find_candidates(text):
    """본문에서 전문용어 후보와 첫 등장 위치를 모읍니다."""
    found = {}

    for term in JARGON:
        for m in re.finditer(re.escape(term), text):
            if _is_standalone(text, term, m.start()):
                found[term] = m.start()
                break

    for m in _ACRONYM.finditer(text):
        term = m.group(1)
        if term in ALLOWLIST:
            continue
        found.setdefault(term, m.start())

    for m in _EMBEDDED_EN.finditer(text):
        term = m.group(1)
        if term.upper() in ALLOWLIST or len(term) < 3:
            continue
        found.setdefault(term, m.start(1))

    return found


def check(markdown, teaches=None, known_terms=None):
    """
    Returns:
        {"ok": bool, "undefined": [{term, position, context}], "checked": n, "summary": str}
    """
    teaches = set(teaches or [])
    known = set(known_terms or [])
    # 표기 흔들림 흡수 (대소문자, 공백)
    known_norm = {k.strip().lower() for k in known | teaches}

    text = _strip_code(markdown)
    candidates = find_candidates(text)

    undefined = []
    for term, pos in sorted(candidates.items(), key=lambda kv: kv[1]):
        if term.strip().lower() in known_norm:
            continue
        if _is_defined_near(text, term, pos):
            continue
        line_start = text.rfind("\n", 0, pos) + 1
        line_end = text.find("\n", pos)
        context = text[line_start: line_end if line_end != -1 else len(text)].strip()
        undefined.append({"term": term, "position": pos, "context": context[:160]})

    return {
        "ok": not undefined,
        "undefined": undefined,
        "checked": len(candidates),
        "summary": f"용어 후보 {len(candidates)}개 / 설명 없이 등장 {len(undefined)}개",
    }


def format_problems(undefined):
    """모델에게 돌려줄 수정 요청 텍스트."""
    return "\n".join(
        f'- "{u["term"]}" — 첫 등장: {u["context"]}' for u in undefined
    )


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    sample = """
터미널을 열고 명령을 입력합니다. 저장소에 커밋을 남기면 됩니다.

API(프로그램끼리 대화하는 창구)를 호출하면 JSON 형태로 응답이 옵니다.

환경변수란 프로그램 밖에서 값을 넘겨주는 방법을 말합니다.

이때 런타임 오류가 나면 스택 트레이스를 확인하세요.

```python
import os
print(os.environ["API_KEY"])
```
"""
    r = check(sample, teaches=["터미널", "명령어"], known_terms=["저장소", "커밋"])
    print(r["summary"])
    for u in r["undefined"]:
        print(f'  ✗ {u["term"]:<14} · {u["context"][:60]}')
