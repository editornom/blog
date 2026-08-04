"""
토픽 클러스터 관리 — 무엇을 쓸지 정하고, 무엇과 연결할지 정합니다.

[구 방식]
  매일 72시간 이내 뉴스 헤드라인에서 '화제성/기술적 깊이/파급력/실용성' 점수가
  가장 높은 것을 골랐습니다. 그 결과 914편이 서로 아무 관계 없는 낱개 글로
  흩어졌고, 같은 주제가 2주 간격으로 중복 생성되기도 했습니다
  (sd-wan-to-sase-evolution-risks 가 5/16, 5/30 두 번).

[신 방식]
  topics.yaml 의 클러스터 중 가장 얇은 것을 골라, 그 안에서 아직 답하지 않은
  질문을 찾습니다. 화제성이 아니라 '이 영역에서 아직 비어 있는 답'이 기준입니다.
  글이 쌓이면 같은 클러스터끼리 서로 연결되어 토픽 클러스터가 자랍니다.
"""

import os
import re
import glob
import json
import datetime

import yaml

import models
from api_utils import gemini_retry, gemini_limiter, gemini_tracker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topics.yaml")
POSTS_DIR = os.path.join(BASE_DIR, "src", "data", "blog", "ko", "posts")


# ── 설정 ────────────────────────────────────────────────────────────
def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def all_clusters(cfg):
    return list(cfg.get("clusters", [])) + [cfg["fallback_cluster"]]


def cluster_by_id(cfg, cid):
    for c in all_clusters(cfg):
        if c["id"] == cid:
            return c
    return None


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


def published_posts():
    """발행된 한국어 포스트의 (cluster, title, slug, date) 목록."""
    out = []
    for path in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        fm = _frontmatter(path)
        if not fm or fm.get("draft"):
            continue
        out.append({
            "cluster": fm.get("cluster") or "general",
            "title": fm.get("title", ""),
            "slug": fm.get("slug", ""),
            "question": fm.get("question", ""),
            "path": path,
            "mtime": os.path.getmtime(path),
        })
    out.sort(key=lambda p: p["mtime"], reverse=True)
    return out


def cluster_counts(cfg, posts=None):
    posts = published_posts() if posts is None else posts
    counts = {c["id"]: 0 for c in all_clusters(cfg)}
    for p in posts:
        counts[p["cluster"]] = counts.get(p["cluster"], 0) + 1
    return counts


def thinnest_cluster(cfg, posts=None):
    """
    글이 가장 적은 클러스터를 고릅니다. 동수면 가장 오래 손대지 않은 쪽입니다.
    fallback(general) 은 의도적으로 채우는 대상이 아니므로 제외합니다.
    """
    posts = published_posts() if posts is None else posts
    counts = cluster_counts(cfg, posts)
    last_touch = {}
    for p in posts:
        last_touch.setdefault(p["cluster"], p["mtime"])

    candidates = cfg.get("clusters", [])
    return min(
        candidates,
        key=lambda c: (counts.get(c["id"], 0), last_touch.get(c["id"], 0.0)),
    )


# ── 주제 선정 ────────────────────────────────────────────────────────
def is_news_day(cfg, when=None):
    """뉴스 기반 글을 쓰는 요일인지. KST 기준."""
    kst = datetime.timezone(datetime.timedelta(hours=9))
    now = when or datetime.datetime.now(kst)
    return now.isoweekday() in set(cfg.get("news_weekdays", []))


def _client():
    from google import genai
    key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=key) if key else None


def propose_question(cluster, existing, headlines=None):
    """
    클러스터 안에서 아직 답하지 않은 질문 하나와, 그 답을 찾을 검색 키워드를 뽑습니다.

    Returns:
        {"question": ..., "search_keyword": ..., "why": ...} 또는 None
    """
    client = _client()
    if client is None:
        return None

    covered = "\n".join(f"- {t}" for t in existing) or "- (아직 이 영역에 발행된 글이 없습니다)"
    news_block = ""
    if headlines:
        news_block = (
            "\n[최근 뉴스 헤드라인 — 이 중 이 영역과 관련된 것이 있으면 질문의 계기로 삼아라]\n"
            + headlines[:6000]
        )

    prompt = f"""
너는 기술 블로그의 콘텐츠 기획자다. 아래 영역에서 **아직 답하지 않은 질문 하나**를 찾아라.

[영역]
{cluster['hub']}

[이 글을 읽을 사람]
{cluster['reader']}

[이 영역에 이미 발행된 글]
{covered}
{news_block}

[규칙]
1. question 은 이 사람이 실제로 검색창에 칠 법한, 물음표로 끝나는 하나의 질문이어야 한다.
   - 나쁜 예: "제로 트러스트의 모든 것" (질문이 아니다)
   - 나쁜 예: "제로 트러스트는 혁신인가 함정인가?" (의견 칼럼 주제다)
   - 좋은 예: "제로 트러스트 세그멘테이션을 기존 VLAN 분리 위에 얹을 수 있나?"
2. **이미 발행된 글과 겹치지 않아야 한다.** 표현만 바꾼 같은 질문을 만들지 마라.
3. 6개월 뒤에 읽어도 유효한 질문을 우선하라. 특정 제품의 이번 주 가격 같은 것은 피하라.
4. search_keyword 는 이 질문의 답을 웹에서 찾기 위한 검색어다. 한국어 또는 영어 6단어 이내.
5. 답이 존재하지 않을 법한 질문(추측성 미래 예측 등)을 만들지 마라.

[출력 — JSON 만]
{{"question": "...", "search_keyword": "...", "why": "이 질문을 고른 이유 한 문장"}}
"""

    @gemini_retry
    def call():
        gemini_limiter.consume()
        return client.models.generate_content(model=models.MAIN, contents=prompt)

    try:
        resp = call()
        gemini_tracker.add_text_usage(resp)
        text = resp.text.strip()
        if "```" in text:
            text = re.sub(r'^```(?:json)?|```$', '', text, flags=re.MULTILINE).strip()
        data = json.loads(text)
        if not data.get("search_keyword"):
            return None
        return data
    except Exception as e:
        print(f"  ⚠️ 질문 도출 실패: {e}")
        return None


def select_topic(headlines_text=None, force_cluster=None):
    """
    오늘 쓸 주제를 정합니다.

    Returns:
        {"cluster": <id>, "hub": ..., "question": ..., "search_keyword": ..., "why": ...}
        또는 None
    """
    cfg = load_config()
    posts = published_posts()
    counts = cluster_counts(cfg, posts)

    if force_cluster:
        cluster = cluster_by_id(cfg, force_cluster)
        if cluster is None:
            print(f"  ⚠️ 알 수 없는 클러스터 '{force_cluster}' — 자동 선정으로 넘어갑니다.")
            cluster = thinnest_cluster(cfg, posts)
    else:
        cluster = thinnest_cluster(cfg, posts)

    print("\n📚 토픽 클러스터 현황")
    for c in cfg["clusters"]:
        mark = "←" if c["id"] == cluster["id"] else " "
        print(f"   {mark} {c['id']:<20} {counts.get(c['id'], 0):>3}편  {c['hub']}")
    if counts.get("general"):
        print(f"     {'general':<20} {counts['general']:>3}편  (클러스터 미분류)")

    existing = [p["question"] or p["title"] for p in posts if p["cluster"] == cluster["id"]]
    use_news = headlines_text and is_news_day(cfg)
    if use_news:
        print("   · 오늘은 뉴스 반영일입니다 — 헤드라인을 질문의 계기로 참고합니다.")

    proposal = propose_question(cluster, existing, headlines_text if use_news else None)
    if not proposal:
        return None

    result = {
        "cluster": cluster["id"],
        "hub": cluster["hub"],
        "reader": cluster["reader"],
        "question": proposal["question"],
        "search_keyword": proposal["search_keyword"],
        "why": proposal.get("why", ""),
    }
    print(f"\n🎯 선정: [{result['cluster']}] {result['question']}")
    print(f"   검색어: {result['search_keyword']}")
    if result["why"]:
        print(f"   이유: {result['why']}")
    return result


# ── 내부 링크 (토픽 클러스터) ─────────────────────────────────────────
def related_links(cluster_id, exclude_slug=None, limit=3):
    """
    같은 클러스터의 글을 우선 연결합니다.
    기존에는 폴더 안 최신 2편을 기계적으로 붙였기 때문에 서로 무관한 글이
    '함께 읽으면 좋은 글'로 붙었습니다.
    """
    posts = [p for p in published_posts() if p["slug"] and p["slug"] != exclude_slug]
    same = [p for p in posts if p["cluster"] == cluster_id]
    others = [p for p in posts if p["cluster"] != cluster_id]

    picked = same[:limit]
    if len(picked) < limit:
        picked += others[: limit - len(picked)]

    return [{"title": p["title"], "href": f"/ko/posts/{p['slug']}", "same_cluster": p in same}
            for p in picked]


if __name__ == "__main__":
    import sys, io
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    cfg = load_config()
    print(f"클러스터 {len(cfg['clusters'])}개 로드됨")
    counts = cluster_counts(cfg)
    for c in cfg["clusters"]:
        print(f"  {c['id']:<20} {counts.get(c['id'], 0):>3}편")
    print(f"\n뉴스 요일: {cfg['news_weekdays']} (오늘은 뉴스일? {is_news_day(cfg)})")
    print(f"가장 얇은 클러스터: {thinnest_cluster(cfg)['id']}")
