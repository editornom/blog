"""
빌드 실패 진단기.

[변경 이전 — 위험]
  이 스크립트는 빌드 로그를 LLM 에 넘긴 뒤, 모델이 지목한 `file_path` 를
  검증 없이 열어 `fixed_content` 로 통째로 덮어쓰고 곧바로 main 에 push 했습니다.
    · 경로 화이트리스트 없음 — 모델이 scripts/main.py 나 .github/workflows/*.yml 을
      지목해도 그대로 덮어썼습니다
    · diff 검토 없음, 수정 후 재빌드 검증 없음, 롤백 없음
    · contents: write 권한과 GITHUB_TOKEN 이 붙은 채로 동작

[변경 이후]
  진단만 합니다. 소스 파일을 쓰지 않고, 커밋하지 않고, push 하지 않습니다.
  원인 분석을 리포트로 남기고, 가능하면 GitHub 이슈로 올려 사람이 판단하게 합니다.

  자동 수정을 되살리려면 최소한 아래가 함께 있어야 합니다.
    1) 수정 가능 경로 화이트리스트 (예: src/data/blog/**.md 만)
    2) 수정 후 재빌드 통과 확인
    3) main 직접 push 가 아닌 PR 생성
"""

import os
import re
import json
import datetime
import subprocess

from dotenv import load_dotenv
from google import genai

import models

load_dotenv()

LOG_PATH = "build_log.txt"
REPORT_DIR = "reports"

# 리포트에 참고 정보로만 넣습니다. 이 스크립트는 어떤 파일도 수정하지 않습니다.
LIKELY_CONTENT_PATH = re.compile(r'src/data/blog/[^\s:"\']+\.md')


def read_log():
    if not os.path.exists(LOG_PATH):
        print("No build log found. Skipping healer.")
        return None
    with open(LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def diagnose(logs):
    """빌드 로그에서 원인과 조치 방안을 뽑습니다. 파일은 건드리지 않습니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    fallback_suspects = sorted(set(LIKELY_CONTENT_PATH.findall(logs)))[:10]

    if not api_key:
        return {"summary": "GEMINI_API_KEY 없음 — 자동 진단을 건너뛰었습니다.",
                "root_cause": "", "suspect_files": fallback_suspects,
                "suggested_fix": "빌드 로그를 직접 확인하세요."}

    client = genai.Client(api_key=api_key)

    prompt = f"""
너는 CI 빌드 실패를 분석하는 진단 도구다. **너는 파일을 수정하지 않는다.**
아래 빌드 로그를 읽고 원인을 특정해서 보고만 하라.

[빌드 로그]
{logs[-20000:]}

[출력 형식 — JSON 만 출력]
{{
  "summary": "한 문장 요약",
  "root_cause": "원인 설명. 로그에서 근거가 된 줄을 인용할 것",
  "suspect_files": ["의심되는 파일 경로"],
  "suggested_fix": "사람이 수행할 구체적 조치. 명령어가 있으면 함께"
}}

[규칙]
- 로그에 근거가 없는 추측을 사실처럼 쓰지 마라. 모르면 root_cause 에 '로그만으로 특정 불가'라고 적어라.
- 수정된 파일 내용을 출력하지 마라. 이 도구는 진단만 한다.
"""

    try:
        resp = client.models.generate_content(model=models.MAIN, contents=prompt)
        text = resp.text.strip()
        if "```" in text:
            text = re.sub(r'^```(?:json)?|```$', '', text, flags=re.MULTILINE).strip()
        diag = json.loads(text)
        if not diag.get("suspect_files"):
            diag["suspect_files"] = fallback_suspects
        return diag
    except Exception as e:
        return {"summary": f"자동 진단 실패: {e}", "root_cause": "",
                "suspect_files": fallback_suspects,
                "suggested_fix": "빌드 로그를 직접 확인하세요."}


def write_report(diag, logs):
    os.makedirs(REPORT_DIR, exist_ok=True)
    now = datetime.datetime.now()
    path = os.path.join(REPORT_DIR, f"build-failure-{now.strftime('%Y-%m-%d_%H%M%S')}.md")

    suspects = "\n".join(f"- `{p}`" for p in (diag.get("suspect_files") or [])) or "- (특정하지 못함)"
    tail = "\n".join(logs.splitlines()[-200:])

    body = f"""# 빌드 실패 진단 ({now.strftime('%Y-%m-%d %H:%M:%S')})

## 요약
{diag.get('summary', '')}

## 원인
{diag.get('root_cause', '')}

## 의심 파일
{suspects}

## 권장 조치
{diag.get('suggested_fix', '')}

> 이 도구는 진단만 수행합니다. 파일을 수정하거나 push 하지 않습니다.

<details><summary>빌드 로그 (마지막 200줄)</summary>

```
{tail}
```

</details>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"📝 진단 리포트 저장: {path}")
    return path, body


def open_issue(title, body):
    """gh CLI 가 있으면 이슈를 생성합니다. 실패해도 무시합니다."""
    if not os.getenv("GITHUB_TOKEN"):
        print("GITHUB_TOKEN 없음 — 이슈 생성을 건너뜁니다.")
        return False
    try:
        subprocess.run(
            ["gh", "issue", "create", "--title", title, "--body", body],
            check=True, capture_output=True, text=True, timeout=60,
        )
        print("🐙 GitHub 이슈를 생성했습니다.")
        return True
    except FileNotFoundError:
        print("gh CLI 를 찾을 수 없어 이슈 생성을 건너뜁니다.")
    except Exception as e:
        print(f"이슈 생성 실패(무시하고 진행): {e}")
    return False


def main():
    logs = read_log()
    if logs is None:
        return 0

    print("--- 빌드 로그 진단 중 (파일 수정 없음) ---")
    diag = diagnose(logs)
    print(f"요약: {diag.get('summary', '')}")

    _, body = write_report(diag, logs)
    open_issue(f"빌드 실패: {diag.get('summary', '원인 미상')[:80]}", body)

    # 실패는 실패로 남깁니다. 조용히 고쳐서 덮는 동작을 하지 않습니다.
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
