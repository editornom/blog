"""
선생 에이전트 — 오늘 무엇을 가르칠지 정합니다.

[기존 topics.py 와의 차이]
  topics.py 는 '글이 가장 적은 클러스터'를 골랐습니다. 정보성 요약은 순서가
  없으니 그래도 됐습니다.
  교육은 순서가 있습니다. 터미널을 모르는 사람에게 환경변수를 설명할 수 없고,
  변수를 모르는 사람에게 함수를 설명할 수 없습니다.
  그래서 여기서는 '선수 지식이 모두 발행된 레슨' 중에서만 고릅니다.

[선정 규칙]
  1. 아직 안 쓴 레슨 중, prerequisites 가 전부 발행 완료인 것만 후보
  2. 후보 중 트랙 균형을 고려 (최근 N편과 같은 트랙이면 감점)
  3. 같은 조건이면 커리큘럼에 먼저 적힌 순서
  4. 후보가 없으면 중단 — 커리큘럼을 다 썼거나 선수 지식이 막혀 있다는 뜻
"""

import os
import glob

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRICULUM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "curriculum.yaml")
POSTS_DIR = os.path.join(BASE_DIR, "src", "data", "blog", "ko", "posts")


def load_curriculum():
    with open(CURRICULUM_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── 커리큘럼 무결성 검사 ─────────────────────────────────────────────
def validate_curriculum(cur):
    """사람이 손으로 고치는 파일이므로 구조를 검사합니다."""
    problems = []
    lessons = cur.get("lessons", [])
    ids = [l["id"] for l in lessons]
    track_ids = {t["id"] for t in cur.get("tracks", [])}

    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"레슨 id 중복: {sorted(dupes)}")

    known = set(ids)
    for l in lessons:
        if l.get("track") not in track_ids:
            problems.append(f"{l['id']}: 알 수 없는 트랙 '{l.get('track')}'")
        for p in l.get("prerequisites", []) or []:
            if p not in known:
                problems.append(f"{l['id']}: 존재하지 않는 선수 레슨 '{p}'")
        if l.get("stack") not in ("none", "web", "python", "shell"):
            problems.append(f"{l['id']}: 알 수 없는 stack '{l.get('stack')}'")

    # 순환 의존 검사 (위상 정렬)
    dep = {l["id"]: set(l.get("prerequisites", []) or []) for l in lessons}
    resolved = set()
    progress = True
    while progress:
        progress = False
        for lid, deps in dep.items():
            if lid not in resolved and deps <= resolved:
                resolved.add(lid)
                progress = True
    stuck = set(dep) - resolved
    if stuck:
        problems.append(f"순환 의존 또는 도달 불가 레슨: {sorted(stuck)}")

    if not any(not (l.get("prerequisites") or []) for l in lessons):
        problems.append("진입점(선수 지식 없는 레슨)이 하나도 없습니다")

    return problems


# ── 발행 현황 ────────────────────────────────────────────────────────
def _frontmatter(path):
    try:
        text = open(path, encoding="utf-8").read()
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except Exception:
        return None


def published_lessons():
    """발행된 레슨 목록. 최신순."""
    out = []
    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        fm = _frontmatter(path)
        if not fm or fm.get("draft"):
            continue
        lid = fm.get("cluster")
        if not lid:
            continue
        out.append({
            "id": lid,
            "title": fm.get("title", ""),
            "slug": fm.get("slug", ""),
            "goal": fm.get("question", ""),
            "mtime": os.path.getmtime(path),
        })
    out.sort(key=lambda p: p["mtime"], reverse=True)
    return out


def taught_terms(cur, published=None):
    """지금까지 발행된 레슨이 설명한 용어 전부. jargon 게이트가 씁니다."""
    published = published_lessons() if published is None else published
    done = {p["id"] for p in published}
    terms: set = set()
    for l in cur["lessons"]:
        if l["id"] in done:
            terms.update(l.get("teaches", []) or [])
    return terms


# ── 다음 레슨 선정 ───────────────────────────────────────────────────
def next_lesson(cur=None, published=None, force_id=None):
    """
    Returns:
        (lesson, context) 또는 (None, 사유)
        context: 학습 목표 / 선수 레슨 링크 / 이미 가르친 용어 / 트랙 정보
    """
    cur = cur or load_curriculum()
    published = published_lessons() if published is None else published

    by_id = {l["id"]: l for l in cur["lessons"]}
    published_by_id = {p["id"]: p for p in published}
    # 커리큘럼에 없는 id(이전 컨셉의 글 등)는 진도에 넣지 않습니다.
    done = {p["id"] for p in published} & set(by_id)

    if force_id:
        lesson = by_id.get(force_id)
        if not lesson:
            return None, f"알 수 없는 레슨 id: {force_id}"
        missing = [p for p in (lesson.get("prerequisites") or []) if p not in done]
        if missing:
            print(f"  ⚠️ 선수 레슨 미발행: {missing} — 지정에 따라 그대로 진행합니다.")
    else:
        candidates = [
            l for l in cur["lessons"]
            if l["id"] not in done and set(l.get("prerequisites") or []) <= done
        ]
        if not candidates:
            remaining = [l["id"] for l in cur["lessons"] if l["id"] not in done]
            if not remaining:
                return None, "커리큘럼의 모든 레슨을 발행했습니다."
            return None, (f"선수 지식이 충족된 레슨이 없습니다. "
                          f"남은 레슨 {len(remaining)}개가 모두 미발행 선수 레슨에 막혀 있습니다.")

        window = cur.get("track_balance_window", 3)
        recent_tracks = [by_id.get(p["id"], {}).get("track") for p in published[:window]]
        order = {l["id"]: i for i, l in enumerate(cur["lessons"])}

        # 트랙별 발행 수. 이게 1순위 기준입니다.
        # 최근 N편 감점만 쓰면, 커리큘럼에 늦게 적힌 트랙이 영영 선택되지 않습니다.
        # (앞 24편에 IT 일반 교양이 한 번도 안 나오는 문제)
        track_done = {t["id"]: 0 for t in cur["tracks"]}
        for p in published:
            tid = by_id.get(p["id"], {}).get("track")
            if tid in track_done:
                track_done[tid] += 1

        def score(l):
            return (
                track_done[l["track"]],              # 가장 뒤처진 트랙 우선
                recent_tracks.count(l["track"]),     # 직전 N편과 겹치면 뒤로
                order[l["id"]],                      # 같으면 커리큘럼 순서
            )

        lesson = min(candidates, key=score)

    track = next((t for t in cur["tracks"] if t["id"] == lesson["track"]), {})
    prereq_links = []
    for pid in lesson.get("prerequisites") or []:
        p = published_by_id.get(pid)
        if p and p.get("slug"):
            prereq_links.append({"id": pid, "title": p["title"], "href": f"/ko/posts/{p['slug']}"})

    context = {
        "lesson_id": lesson["id"],
        "track": lesson["track"],
        "track_name": track.get("name", lesson["track"]),
        "goal": lesson["goal"],
        "stack": lesson.get("stack", "none"),
        "teaches": lesson.get("teaches", []) or [],
        "prerequisites": prereq_links,
        "known_terms": sorted(taught_terms(cur, published)),
        "progress": f"{len(done)}/{len(cur['lessons'])}",
    }
    return lesson, context


def print_status(cur=None, published=None):
    cur = cur or load_curriculum()
    published = published_lessons() if published is None else published
    ids = {l["id"] for l in cur["lessons"]}
    done = {p["id"] for p in published} & ids
    orphans = [p for p in published if p["id"] not in ids]

    print("\n📚 커리큘럼 진도")
    for t in cur["tracks"]:
        ls = [l for l in cur["lessons"] if l["track"] == t["id"]]
        n = sum(1 for l in ls if l["id"] in done)
        bar = "█" * n + "·" * (len(ls) - n)
        print(f"   {t['name']:<16} {bar} {n}/{len(ls)}")
    print(f"   전체 {len(done)}/{len(cur['lessons'])}편")
    if orphans:
        print(f"   ⚠️ 커리큘럼 밖의 글 {len(orphans)}편: "
              f"{', '.join(p['id'] for p in orphans[:5])} (진도에 포함하지 않음)")


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    cur = load_curriculum()
    problems = validate_curriculum(cur)
    if problems:
        print("❌ 커리큘럼 구조 문제")
        for p in problems:
            print(f"   · {p}")
        raise SystemExit(1)
    print(f"✅ 커리큘럼 검사 통과 — 트랙 {len(cur['tracks'])}개 / 레슨 {len(cur['lessons'])}개")

    print_status(cur)
    lesson, ctx = next_lesson(cur)
    if lesson is None:
        print(f"\n🛑 {ctx}")
    else:
        print(f"\n🎯 다음 레슨: [{ctx['track_name']}] {lesson['id']}")
        print(f"   목표: {ctx['goal']}")
        print(f"   스택: {ctx['stack']}  |  새 용어: {', '.join(ctx['teaches'])}")
        print(f"   선수: {[p['id'] for p in ctx['prerequisites']] or '없음 (진입점)'}")
        print(f"   이미 가르친 용어 {len(ctx['known_terms'])}개")
