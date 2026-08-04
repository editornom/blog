"""
본문 도해 렌더러 — 결정론적, 모델 미개입.

[왜 이미지 생성을 대체하는가]
기존 파이프라인은 본문에 `[이미지: A circular flow diagram illustrating the four
stages...]` 같은 프롬프트를 넣고 Imagen 으로 뽑았습니다. 그런데 이건 다이어그램
요청이고, 생성 모델은 도해 안의 글자를 정확히 그리지 못합니다. 결과물은 본문과
무관한 추상 이미지였고 장당 과금됐습니다.

[왜 SVG 가 아니라 HTML/CSS 인가]
SVG 는 좌표가 고정입니다. 같은 도해를 en/jp/cn 으로 번역하면 텍스트 길이가 바뀌어
박스를 넘치거나 겹칩니다. HTML/CSS 는 브라우저가 재배치하므로 번역에 안전하고,
반응형이며, 다크모드가 CSS 한 줄로 해결되고, 텍스트가 실제 텍스트라 접근성·검색에
그대로 잡힙니다. astro.config.ts 에 rehypeRaw 가 이미 켜져 있어 본문에 그대로 들어갑니다.

(대표 이미지 ogImage 는 실제 이미지 파일이 필요하므로 기존 satori 경로를 그대로 씁니다.)

[본문 표기법]
    [도해: flow  | 실험 및 프로토타입 > 파인튜닝 > 배포 및 통합 > 모니터링]
    [도해: stack | 응용 계층 > 오케스트레이션 > 모델 계층 > 인프라]
    [도해: cycle | 수집 > 학습 > 배포 > 관측]

각 항목에 `::` 로 한 줄 설명을 붙일 수 있습니다.
    [도해: flow | 실험::모델·프롬프트 비교 > 배포::API 레이어 구성]
"""

import re
from html import escape

TYPES = {
    "flow": "순서",
    "stack": "계층",
    "cycle": "순환",
}

MIN_ITEMS = 2
MAX_ITEMS = 6

# [도해: flow | a > b > c]  — 대괄호 안, 유형과 항목을 | 로 구분
_SPEC_RE = re.compile(
    r'(?:\*\*|_)?!?\\?\[\s*도해\s*:\s*([a-zA-Z]+)\s*\|\s*([^\]]+?)\s*\\?\](?:\*\*|_)?'
)


def parse_items(raw):
    """'a::설명 > b > c' → [(label, desc), ...]"""
    items = []
    for chunk in raw.split(">"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "::" in chunk:
            label, desc = chunk.split("::", 1)
        else:
            label, desc = chunk, ""
        label = label.strip()
        if label:
            items.append((label, desc.strip()))
    return items


def render(kind, items):
    """도해 HTML 을 한 줄로 반환합니다.

    마크다운은 빈 줄을 만나면 HTML 블록에서 빠져나오므로, 내부에 줄바꿈을
    넣지 않고 한 줄로 출력합니다.
    """
    kind = kind.lower()
    if kind not in TYPES:
        return None
    if not (MIN_ITEMS <= len(items) <= MAX_ITEMS):
        return None

    label_text = " → ".join(label for label, _ in items)
    aria = escape(f"{TYPES[kind]} 도해: {label_text}", quote=True)

    lis = []
    for label, desc in items:
        inner = f'<b class="dgm-label">{escape(label)}</b>'
        if desc:
            inner += f'<span class="dgm-desc">{escape(desc)}</span>'
        lis.append(f'<li class="dgm-item">{inner}</li>')

    return (
        f'<figure class="dgm dgm-{kind}" role="group" aria-label="{aria}">'
        f'<ol class="dgm-items">{"".join(lis)}</ol>'
        f'</figure>'
    )


def replace_placeholders(markdown):
    """
    본문의 [도해: ...] 표기를 HTML 로 치환합니다.

    Returns:
        (markdown, rendered_count, dropped_specs)
        해석할 수 없는 표기는 조용히 두지 않고 제거 목록으로 돌려줍니다.
        (본문에 원시 표기가 남아 독자에게 노출되는 것을 막습니다)
    """
    rendered = 0
    dropped = []

    def _sub(m):
        nonlocal rendered
        kind, raw = m.group(1), m.group(2)
        html = render(kind, parse_items(raw))
        if html is None:
            dropped.append(m.group(0))
            return ""
        rendered += 1
        # 앞뒤로 빈 줄을 확보해야 마크다운이 블록 HTML 로 인식합니다.
        return f"\n\n{html}\n\n"

    out = _SPEC_RE.sub(_sub, markdown)
    out = re.sub(r'\n{4,}', '\n\n\n', out)
    return out, rendered, dropped


def has_placeholder(markdown):
    return bool(_SPEC_RE.search(markdown))


if __name__ == "__main__":
    import sys, io
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    sample = """앞 문단입니다.

[도해: flow | 실험 및 프로토타입::모델·프롬프트 비교 > 파인튜닝 및 최적화 > 배포 및 통합::API 레이어 구성 > 모니터링 및 지속 개선]

가운데 문단입니다.

[도해: stack | 응용 계층 > 오케스트레이션 > 모델 계층 > 인프라]

[도해: bogus | 하나]

뒤 문단입니다.
"""
    out, n, dropped = replace_placeholders(sample)
    print(out)
    print(f"--- 렌더 {n}건 / 폐기 {len(dropped)}건: {dropped}")
