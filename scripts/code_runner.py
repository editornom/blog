"""
예시 코드 검증 — 이 블로그의 새 진실 기준.

[왜 verifier.py 를 대신하나]
  기존 verifier 는 '본문의 수치가 소스 원문에 있는가'를 봤습니다.
  웹 자료를 요약하는 글이었으니 그게 맞았습니다.

  교육 콘텐츠는 요약이 아니라 설명입니다. "for 문은 반복을 수행합니다"에
  소스 대조는 의미가 없습니다. 대신 초보자에게 치명적인 실패는 따로 있습니다.

      예시 코드가 안 돌아간다

  초보자는 코드가 안 돌면 자기가 틀린 줄 알고 좌절합니다. 그러니 발행 전에
  실제로 돌려봅니다. 이것이 이 파이프라인에서 가장 중요한 게이트입니다.

[코드블록 표기 규칙]
  블록의 첫 줄 주석으로 의도를 표시합니다. 독자에게도 그대로 보입니다.

      ```python
      # 잘못된 예 — 실행하면 오류가 납니다
      print(name)
      ```
      → 실행해서 '실패해야' 통과. 멀쩡히 돌면 그것도 오류로 잡습니다.

      ```python
      # 실행 생략 — API 키가 필요합니다
      ```
      → 구문 검사만 합니다.

      (표시 없음)
      → 그대로 실행되어야 합니다. 독자가 복붙할 코드이기 때문입니다.

[셸 명령]
  실행하지 않습니다. 대신 위험 명령을 차단합니다.
  초보자는 블로그의 명령을 그대로 붙여넣기 때문에, 파괴적인 명령이 섞이면
  그 자체가 사고입니다.
"""

import os
import re
import json
import shutil
import subprocess
import tempfile

TIMEOUT_SEC = 15

# 첫 줄 주석 마커
_BAD_MARKER = re.compile(r'^\s*(?:#|//|<!--)\s*.*(잘못된\s*예|오류\s*예|안\s*되는\s*예)', re.I)
_SKIP_MARKER = re.compile(r'^\s*(?:#|//|<!--)\s*.*(실행\s*생략|실행하지\s*마)', re.I)

# ```lang ... ``` 코드블록
_FENCE_RE = re.compile(r'^```([^\n`]*)\n(.*?)^```', re.MULTILINE | re.DOTALL)

PY_ALIASES = {"python", "py", "python3"}
JS_ALIASES = {"javascript", "js", "node", "nodejs"}
SHELL_ALIASES = {"bash", "sh", "shell", "zsh", "console", "terminal"}
SYNTAX_ONLY = {"json", "yaml", "yml", "html", "css", "sql", "xml", "toml", "ini", "env", "dotenv",
               "text", "txt", "diff", "markdown", "md"}

# 초보자가 그대로 붙여넣으면 사고가 나는 명령들
DANGEROUS = [
    (r'\brm\s+(-[a-zA-Z]*\s+)*-?[a-zA-Z]*[rf][a-zA-Z]*\s+/', "루트 경로를 지우는 rm"),
    (r'\brm\s+-rf\s+[~*]', "홈/와일드카드를 지우는 rm -rf"),
    (r'\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba)?sh', "내려받은 스크립트를 바로 실행(curl | sh)"),
    (r'\bsudo\b', "sudo (권한 상승)"),
    (r'\bchmod\s+(-R\s+)?777\b', "chmod 777 (모든 권한 개방)"),
    (r'\bmkfs\b', "파일시스템 포맷"),
    (r'\bdd\s+if=', "dd (디스크 직접 쓰기)"),
    (r'>\s*/dev/(sd|nvme|disk)', "블록 디바이스에 직접 쓰기"),
    (r':\(\)\s*\{.*\|.*&\s*\}\s*;', "포크 폭탄"),
    (r'\bgit\s+push\s+(-f|--force)\b', "강제 푸시"),
    (r'\bgit\s+reset\s+--hard\b', "git reset --hard (되돌릴 수 없는 변경 삭제)"),
    (r'\beval\s*\(', "eval (임의 코드 실행)"),
    (r'\bos\.system\s*\(', "os.system (셸 직접 호출)"),
]


class Block:
    def __init__(self, lang, code, start, end, raw):
        self.lang = (lang or "").strip().split()[0].lower() if (lang or "").strip() else ""
        self.code = code
        self.start = start
        self.end = end
        self.raw = raw
        first = code.strip().split("\n", 1)[0] if code.strip() else ""
        self.expect_fail = bool(_BAD_MARKER.search(first))
        self.skip_run = bool(_SKIP_MARKER.search(first))

    @property
    def kind(self):
        if self.lang in PY_ALIASES:
            return "python"
        if self.lang in JS_ALIASES:
            return "javascript"
        if self.lang in SHELL_ALIASES:
            return "shell"
        if self.lang in SYNTAX_ONLY:
            return "syntax"
        return "unknown"


def extract_blocks(markdown):
    blocks = []
    for m in _FENCE_RE.finditer(markdown):
        blocks.append(Block(m.group(1), m.group(2), m.start(), m.end(), m.group(0)))
    return blocks


# ── 개별 검사 ────────────────────────────────────────────────────────
def _run(cmd, cwd, stdin_file=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=TIMEOUT_SEC, encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "", f"{TIMEOUT_SEC}초 안에 끝나지 않았습니다 (무한 루프 가능성)"
    except FileNotFoundError as e:
        return 127, "", f"실행기를 찾을 수 없습니다: {e}"


def check_python(code, workdir, run=True):
    path = os.path.join(workdir, "snippet.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    if not run:
        try:
            compile(code, "snippet.py", "exec")
            return True, ""
        except SyntaxError as e:
            return False, f"구문 오류 {e.lineno}행: {e.msg}"
    import sys
    rc, out, err = _run([sys.executable, path], workdir)
    return rc == 0, err.strip() or out.strip()


def check_javascript(code, workdir, run=True):
    node = shutil.which("node")
    if not node:
        return None, "node 를 찾을 수 없어 검사를 건너뜁니다"
    path = os.path.join(workdir, "snippet.mjs")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    cmd = [node, "--check", path] if not run else [node, path]
    rc, out, err = _run(cmd, workdir)
    return rc == 0, err.strip() or out.strip()


def check_syntax_only(lang, code):
    try:
        if lang in ("json",):
            json.loads(code)
        elif lang in ("yaml", "yml"):
            import yaml
            yaml.safe_load(code)
        elif lang in ("html", "xml"):
            from html.parser import HTMLParser

            class P(HTMLParser):
                pass
            P().feed(code)
        return True, ""
    except Exception as e:
        return False, str(e)


def scan_dangerous(code):
    hits = []
    for pattern, label in DANGEROUS:
        if re.search(pattern, code):
            hits.append(label)
    return hits


# ── 전체 검사 ────────────────────────────────────────────────────────
def check(markdown):
    """
    Returns:
        {"ok": bool, "blocks": n, "problems": [ {block, lang, reason, detail} ], "summary": str}
    """
    blocks = extract_blocks(markdown)
    problems = []
    ran = 0

    with tempfile.TemporaryDirectory(prefix="lesson_code_") as workdir:
        for i, b in enumerate(blocks, 1):
            if not b.lang:
                problems.append({
                    "block": i, "lang": "(없음)", "reason": "언어 태그 없음",
                    "detail": "코드블록에 언어를 표시해야 문법 강조가 됩니다. 초보자에게는 이게 큽니다.",
                    "code": b.code[:200],
                })
                continue

            danger = scan_dangerous(b.code)
            if danger and not b.expect_fail:
                problems.append({
                    "block": i, "lang": b.lang, "reason": "위험한 명령",
                    "detail": "독자가 그대로 붙여넣습니다: " + ", ".join(danger),
                    "code": b.code[:200],
                })
                continue

            kind = b.kind
            if kind == "shell":
                continue  # 위험 검사만 하고 실행하지 않습니다
            if kind == "unknown":
                continue  # 모르는 언어는 통과시킵니다 (astro, jsx 등)
            if kind == "syntax":
                ok, detail = check_syntax_only(b.lang, b.code)
                if not ok and not b.expect_fail:
                    problems.append({"block": i, "lang": b.lang, "reason": "구문 오류",
                                     "detail": detail, "code": b.code[:200]})
                continue

            should_run = not b.skip_run
            if kind == "python":
                ok, detail = check_python(b.code, workdir, run=should_run)
            else:
                ok, detail = check_javascript(b.code, workdir, run=should_run)

            if ok is None:  # 실행기 없음
                continue
            ran += 1

            if b.expect_fail:
                if ok:
                    problems.append({
                        "block": i, "lang": b.lang, "reason": "잘못된 예인데 정상 실행됨",
                        "detail": "'잘못된 예'로 표시했는데 오류 없이 돌아갑니다. 표시를 지우거나 예시를 고치세요.",
                        "code": b.code[:200],
                    })
            elif not ok:
                problems.append({
                    "block": i, "lang": b.lang,
                    "reason": "실행 실패" if should_run else "구문 오류",
                    "detail": detail[:600], "code": b.code[:200],
                })

    summary = f"코드블록 {len(blocks)}개 (실행 {ran}개) / 문제 {len(problems)}건"
    return {"ok": not problems, "blocks": len(blocks), "ran": ran,
            "problems": problems, "summary": summary}


def format_problems(problems):
    """모델에게 돌려줄 수정 요청 텍스트."""
    out = []
    for p in problems:
        out.append(
            f"[{p['block']}번 블록 · {p['lang']}] {p['reason']}\n"
            f"  문제: {p['detail']}\n"
            f"  코드: {p['code'][:200]}"
        )
    return "\n\n".join(out)


if __name__ == "__main__":
    import sys, io
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    sample = '''본문입니다.

```python
name = "홍길동"
print(f"안녕하세요, {name}님")
```

```python
# 잘못된 예 — 실행하면 오류가 납니다
print(undefined_name)
```

```
태그 없는 블록
```

```bash
sudo rm -rf /
```

```json
{"a": 1,}
```
'''
    r = check(sample)
    print(r["summary"])
    for p in r["problems"]:
        print(f"  ✗ [{p['block']}] {p['lang']}: {p['reason']} — {p['detail'][:80]}")
