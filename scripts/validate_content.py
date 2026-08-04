"""
1층 기계 검증 — 모델이 개입하지 않는 결정론적 콘텐츠 검사.

평가를 AI에게 맡기기 전에 통과해야 하는 층입니다.
모델의 판단이 들어가지 않으므로 결과가 재현 가능하고, 사람이 반박할 수 없습니다.

검사 항목
  1. 프론트매터 필수 필드 / 스키마
  2. slug 중복
  3. 언어별 편수 정합성 (ko / en / jp / cn)
  4. 내부 링크가 실제 존재하는 글을 가리키는가
  5. 이미지 경로가 실제 파일을 가리키는가
  6. 헤딩 레벨 건너뜀 (H1 다음 H3)
  7. 화자 없는 인용구 (독자를 오도하는 가짜 인용)
  8. 태그 미분류 (tags 누락 또는 others)
  9. 본문에 남은 이미지 플레이스홀더

사용:
    python scripts/validate_content.py              # 전체 검사
    python scripts/validate_content.py --lang ko    # 특정 언어만
    python scripts/validate_content.py --quiet      # 요약만
종료 코드: 오류가 하나라도 있으면 1
"""

import os
import re
import sys
import glob
import argparse
from collections import defaultdict

import yaml

BLOG_ROOT = os.path.join("src", "data", "blog")
LANGS = ["ko", "en", "jp", "cn"]
REQUIRED_FIELDS = ["title", "slug", "description", "pubDatetime"]

# 헤딩 레벨, 인용구, 이미지, 내부 링크 패턴
_H_RE = re.compile(r'^(#{1,6})\s+', re.MULTILINE)
_QUOTE_RE = re.compile(r'^>\s*["“](.+?)["”]\s*$', re.MULTILINE)
# 경로에 괄호가 들어가는 경우가 있어(예: MCP_(Model_Context_Protocol)/)
# 확장자를 기준으로 끊습니다. `[^)]+` 로 잡으면 경로가 잘려 오탐이 납니다.
_IMG_RE = re.compile(r'!\[[^\]]*\]\((.+?\.(?:webp|png|jpe?g|gif|svg|avif))\)', re.IGNORECASE)
_INTERNAL_RE = re.compile(r'\]\((/(?:ko|en|jp|cn)/(?:posts|haionnet)/([a-z0-9\-]+))\)')
_PLACEHOLDER_RE = re.compile(r'\[\s*(?:이미지|도해)\s*:')
_DGM_FIG_RE = re.compile(r'<figure class="dgm[^"]*"')
_DGM_ITEM_RE = re.compile(r'<li class="dgm-item">')
_DGM_CLOSE_RE = re.compile(r'</figure>')


class Report:
    def __init__(self):
        self.errors = defaultdict(list)   # 발행을 막아야 하는 문제
        self.warnings = defaultdict(list) # 품질 문제

    def error(self, path, msg):
        self.errors[path].append(msg)

    def warn(self, path, msg):
        self.warnings[path].append(msg)

    @property
    def error_count(self):
        return sum(len(v) for v in self.errors.values())

    @property
    def warning_count(self):
        return sum(len(v) for v in self.warnings.values())


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        return yaml.safe_load(parts[1]), parts[2]
    except Exception:
        return "INVALID", parts[2]


def collect(langs):
    """{lang: {slug: path}} 와 전체 파일 목록을 돌려줍니다."""
    index = {lang: {} for lang in langs}
    files = []
    for lang in langs:
        pattern = os.path.join(BLOG_ROOT, lang, "**", "*.md")
        for path in glob.glob(pattern, recursive=True):
            files.append((lang, path))
    return index, files


def validate(langs, report):
    index, files = collect(langs)
    seen_slug = defaultdict(list)
    counts = defaultdict(lambda: defaultdict(int))

    for lang, path in files:
        rel = path.replace("\\", "/")
        try:
            text = open(path, encoding="utf-8").read()
        except Exception as e:
            report.error(rel, f"파일을 읽을 수 없음: {e}")
            continue

        fm, body = split_frontmatter(text)

        # 1. 프론트매터
        if fm is None:
            report.error(rel, "프론트매터가 없음")
            continue
        if fm == "INVALID":
            report.error(rel, "프론트매터 YAML 파싱 실패")
            continue

        for field in REQUIRED_FIELDS:
            if not fm.get(field):
                report.error(rel, f"필수 필드 누락: {field}")

        slug = fm.get("slug")
        collection = "haionnet" if "/haionnet/" in rel else "posts"
        if slug:
            index[lang][slug] = rel
            seen_slug[(lang, slug)].append(rel)
            counts[lang][collection] += 1

        # 8-1. 토픽 클러스터
        cl = fm.get("cluster")
        if not cl:
            report.warn(rel, "cluster 누락 — 내부 링크와 다음 주제 선정에서 제외됩니다")
        elif cl == "general":
            report.warn(rel, "클러스터 미분류(general) — topics.yaml 에 클러스터 추가를 검토하세요")

        # 8. 태그
        tags = fm.get("tags")
        if not tags:
            report.warn(rel, "tags 누락 (스키마 기본값 others 로 떨어짐)")
        elif isinstance(tags, list) and all(t in ("others", "it", "tech") for t in tags):
            report.warn(rel, f"태그가 분류 정보를 주지 않음: {tags}")

        # 6. 헤딩 레벨 건너뜀
        levels = [len(m.group(1)) for m in _H_RE.finditer(body)]
        for prev, cur in zip(levels, levels[1:]):
            if cur - prev > 1:
                report.warn(rel, f"헤딩 레벨 건너뜀: H{prev} 다음 H{cur}")
                break

        # 7. 화자 없는 인용구
        for m in _QUOTE_RE.finditer(body):
            report.warn(rel, f'화자 없는 인용구: "{m.group(1)[:50]}..."')
            break

        # 9. 남은 플레이스홀더
        if _PLACEHOLDER_RE.search(body):
            report.error(rel, "이미지/도해 플레이스홀더가 치환되지 않고 본문에 남아 있음")

        # 10. 도해 블록 무결성
        #     번역 과정에서 태그가 깨지거나 항목이 사라지는 것을 잡습니다.
        n_fig, n_close = len(_DGM_FIG_RE.findall(body)), len(_DGM_CLOSE_RE.findall(body))
        if n_fig != n_close:
            report.error(rel, f"도해 태그 불일치: <figure class=\"dgm\"> {n_fig}개 vs </figure> {n_close}개")
        if n_fig:
            n_items = len(_DGM_ITEM_RE.findall(body))
            if n_items < n_fig * 2:
                report.error(rel, f"도해 항목 부족: 도해 {n_fig}개에 항목 {n_items}개 (도해당 최소 2개)")
            for m in _DGM_FIG_RE.finditer(body):
                seg = body[m.start():body.find("</figure>", m.start())]
                if "\n\n" in seg:
                    report.error(rel, "도해 블록 안에 빈 줄이 있어 렌더링이 깨집니다")
                    break

        # 5. 이미지 경로
        post_dir = os.path.dirname(path)
        for m in _IMG_RE.finditer(body):
            src = m.group(1).split(" ")[0].strip()
            if src.startswith(("http://", "https://", "data:")):
                continue
            from urllib.parse import unquote
            target = os.path.normpath(os.path.join(post_dir, unquote(src)))
            if not os.path.exists(target):
                report.error(rel, f"이미지 파일 없음: {src}")

    # 2. slug 중복
    for (lang, slug), paths in seen_slug.items():
        if len(paths) > 1:
            report.error(paths[0], f"[{lang}] slug 중복 '{slug}': {len(paths)}개 파일")

    # 4. 내부 링크 유효성 (2차 순회 — 전체 index 가 채워진 뒤)
    for lang, path in files:
        rel = path.replace("\\", "/")
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        _, body = split_frontmatter(text)
        broken = set()
        for m in _INTERNAL_RE.finditer(body):
            href, target_slug = m.group(1), m.group(2)
            target_lang = href.split("/")[1]
            if target_lang in index and target_slug not in index[target_lang]:
                broken.add(href)
        for href in sorted(broken)[:5]:
            report.error(rel, f"내부 링크가 존재하지 않는 글을 가리킴: {href}")

    return counts


def check_language_parity(counts, report):
    """언어별 편수가 어긋나면 번역 누락입니다."""
    print("\n📊 언어별 편수")
    collections = sorted({c for lang in counts for c in counts[lang]})
    base = None
    for collection in collections:
        row = {lang: counts[lang].get(collection, 0) for lang in counts}
        print(f"  {collection:10} " + "  ".join(f"{l}:{n}" for l, n in row.items()))
        values = [n for n in row.values() if n]
        if values and max(values) != min(values):
            missing = {l: max(values) - n for l, n in row.items() if n < max(values)}
            report.warn("(전체)", f"{collection} 편수 불일치 — 번역 누락 추정: {missing}")


BASELINE_PATH = os.path.join("reports", "content-baseline.json")


def fingerprints(report):
    """오류를 파일+메시지 단위로 식별합니다."""
    return {f"{path}::{msg}" for path, msgs in report.errors.items() for msg in msgs}


def load_baseline(path):
    import json
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return set(json.load(f).get("known_errors", []))
    except Exception as e:
        print(f"⚠️ 베이스라인을 읽지 못했습니다({e}). 전체 오류를 기준으로 판정합니다.")
        return None


def save_baseline(path, report):
    import json
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "note": "기존 콘텐츠의 알려진 오류 목록. CI 는 여기 없는 새 오류만 차단합니다. "
                "부채를 갚으면 --write-baseline 으로 다시 만드세요.",
        "count": report.error_count,
        "known_errors": sorted(fingerprints(report)),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 베이스라인 저장: {path} ({report.error_count}건)")


def main():
    parser = argparse.ArgumentParser(description="정보성 콘텐츠 기계 검증 (모델 미개입)")
    parser.add_argument("--lang", help="특정 언어만 검사 (ko/en/jp/cn)")
    parser.add_argument("--quiet", action="store_true", help="요약만 출력")
    parser.add_argument("--baseline", nargs="?", const=BASELINE_PATH,
                        help="알려진 오류를 무시하고 새 오류만 차단 (기본: reports/content-baseline.json)")
    parser.add_argument("--write-baseline", action="store_true",
                        help="현재 오류를 베이스라인으로 기록")
    args = parser.parse_args()

    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    langs = [args.lang] if args.lang else LANGS
    langs = [l for l in langs if os.path.isdir(os.path.join(BLOG_ROOT, l))]
    if not langs:
        print(f"❌ {BLOG_ROOT} 아래에서 콘텐츠를 찾을 수 없습니다. 저장소 루트에서 실행하세요.")
        return 1

    report = Report()
    print("=" * 60)
    print("🔬 1층 기계 검증 (모델 미개입)")
    print("=" * 60)

    counts = validate(langs, report)
    check_language_parity(counts, report)

    if not args.quiet:
        if report.errors:
            print("\n❌ 오류 (발행 차단)")
            for path, msgs in sorted(report.errors.items()):
                print(f"  {path}")
                for m in msgs:
                    print(f"    · {m}")
        if report.warnings:
            print("\n⚠️  경고 (품질)")
            shown = 0
            for path, msgs in sorted(report.warnings.items()):
                if shown >= 40:
                    print(f"  ... 외 {len(report.warnings) - shown}개 파일")
                    break
                print(f"  {path}")
                for m in msgs:
                    print(f"    · {m}")
                shown += 1

    print("\n" + "=" * 60)
    print(f"오류 {report.error_count}건 / 경고 {report.warning_count}건")
    print("=" * 60)

    if args.write_baseline:
        save_baseline(BASELINE_PATH, report)
        return 0

    if args.baseline:
        known = load_baseline(args.baseline)
        if known is not None:
            current = fingerprints(report)
            new_errors = sorted(current - known)
            fixed = len(known - current)
            print(f"\n베이스라인 대비: 신규 오류 {len(new_errors)}건 / 해소 {fixed}건 "
                  f"(알려진 부채 {len(known)}건)")
            if new_errors:
                print("\n❌ 이번 변경으로 새로 생긴 오류:")
                for e in new_errors[:20]:
                    path, msg = e.split("::", 1)
                    print(f"  {path}\n    · {msg}")
                return 1
            print("✅ 새로 생긴 오류 없음")
            return 0

    return 1 if report.error_count else 0


if __name__ == "__main__":
    sys.exit(main())
