import os
import sys
import uuid
import re
import json
import time
import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
from typing import List
from pydantic import BaseModel, Field
import yaml

from crawler import fetch_content, extract_related_links
from generator import generate_blog_post
from reviewer import review_manuscript
from imagen_helper import generate_image
from translator import translate_and_save, translate_text
from publish import push_to_github
from headline_crawler import generate_daily_headlines_file
from trend_catcher import save_keyword_to_history
from search_expert import deep_search_and_filter
from api_utils import gemini_tracker
from google import genai
import models
import verifier
import diagram
import teacher


def slugify_fallback(title):
    """메타데이터 생성이 실패했을 때 쓰는 최소한의 슬러그. 한글은 버리고 영문/숫자만 남깁니다."""
    ascii_only = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', title)
    words = [w for w in ascii_only.lower().split() if w]
    return "-".join(words[:6])


def inject_internal_links(draft, folder, lesson_ctx=None):
    """
    커리큘럼 관계로 글을 연결합니다.

    [1차 수정] 폴더 내 최신 2편 → 같은 토픽 클러스터
    [2차 수정] 교육 콘텐츠에서 의미 있는 연결은 '선수 레슨'과 '다음 레슨'입니다.
               독자가 막히면 앞으로 돌아가야 하고, 이해했으면 다음으로 가야 합니다.
    """
    if folder != "posts" or not lesson_ctx:
        return draft

    blocks = []

    prereq = lesson_ctx.get("prerequisites") or []
    if prereq:
        lines = "\n".join(f"- [{p['title']}]({p['href']})" for p in prereq)
        blocks.append("## 📌 먼저 읽으면 좋은 글\n" + lines)

    try:
        nxt = teacher.upcoming_lessons(lesson_ctx["lesson_id"], limit=2)
    except Exception as e:
        print(f"  ⚠️ 다음 레슨 조회 실패: {e}")
        nxt = []
    if nxt:
        lines = "\n".join(f"- {n['goal']}" for n in nxt)
        blocks.append("## ➡️ 다음에 다룰 내용\n" + lines)

    if not blocks:
        print("  · 연결할 글이 없습니다 (커리큘럼의 시작점)")
        return draft

    draft += "\n\n" + "\n\n".join(blocks) + "\n"
    print(f"  ✅ 내부 링크: 선수 {len(prereq)}편 / 예고 {len(nxt)}건")
    return draft

class PostMeta(BaseModel):
    slug: str = Field(description="영문 소문자와 하이픈만 사용한 짧은 URL 슬러그")
    description: str = Field(description="검색 결과에 노출될 1~2문장 요약. 따옴표·줄바꿈 금지")
    tags: List[str] = Field(description="이 글의 주제를 나타내는 소문자 영문 태그 2~4개 (예: zero-trust, sase)")


def assemble_post_metadata(reviewed_data, folder="posts", keyword="", urls=None, draft=False,
                           cluster=None, question=None):
    """
    Creates final Frontmatter and combines it with refined content.

    [수리] 슬러그·설명·태그를 개별 호출 3회에서 구조화 출력 1회로 통합했습니다.
    [수리] tags 를 실제로 생성합니다. 기존에는 이 필드를 아예 넣지 않아
           content.config.ts 의 기본값 ["others"] 로 떨어졌고, 그 결과
           914편 전부가 같은 태그를 달고 있었습니다.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    title = reviewed_data['title']
    content = reviewed_data['content']

    print(f"  [Assembler] 슬러그 / 메타 설명 / 태그 생성 중...")
    meta_prompt = f"""
아래 기술 문서의 메타데이터를 만들어라.

[제목]
{title}

[본문 앞부분]
{content[:1500]}

[규칙]
- slug: 영문 소문자와 하이픈만. 5단어 이내. 한글 음차 금지.
- description: **반드시 한국어로** 작성하라. 본문이 한국어이므로 검색 결과 설명도 한국어여야 한다.
  이 글이 어떤 질문에 답하는지 알 수 있게 1~2문장. 과장 표현 금지. 따옴표와 줄바꿈 금지.
- tags: 본문에서 실제로 다룬 기술 주제만. 소문자 영문 하이픈 표기. 2~4개.
  ("others", "it", "tech" 처럼 아무 정보도 주지 않는 태그 금지)
"""

    slug = ""
    description = ""
    tags = []
    try:
        meta_resp = client.models.generate_content(
            model=models.FAST,
            contents=meta_prompt,
            config={'response_mime_type': 'application/json', 'response_schema': PostMeta}
        )
        gemini_tracker.add_text_usage(meta_resp)
        meta = json.loads(meta_resp.text)
        slug = re.sub(r'[^a-z0-9\-]', '', meta.get("slug", "").strip().lower().replace(' ', '-'))
        description = meta.get("description", "").strip().replace('"', "'").replace("\n", " ")
        tags = [
            re.sub(r'[^a-z0-9\-]', '', t.strip().lower().replace(' ', '-'))
            for t in (meta.get("tags") or [])
        ]
        tags = [t for t in tags if t and t not in ("others", "it", "tech")][:4]
    except Exception as e:
        print(f"  ⚠️ 메타데이터 생성 실패: {e}")

    if not slug:
        slug = re.sub(r'[^a-z0-9\-]', '', slugify_fallback(title)) or "post"
    if not description:
        description = title
    if not tags:
        tags = ["uncategorized"]

    # 3. Time calculation
    seoul_tz = datetime.timezone(datetime.timedelta(hours=9))
    seoul_now = datetime.datetime.now(seoul_tz)
    pub_time = seoul_now - datetime.timedelta(minutes=10) # Buffer
    prefix = pub_time.strftime("%y%m%d_")
    
    # 4. Assemble YAML
    fm_data = {
        "title": title,
        # 이 블로그는 비개발자가 먼저 배운 것을 기록하는 곳입니다.
        # 'Senior Tech Editor' 같은 권위 표기는 컨셉과 맞지 않습니다.
        "author": "Be Dev.Log",
        "author_url": "https://editornom.com/about",
        "pubDatetime": pub_time, # Pass datetime object directly
        "slug": slug,
        "featured": False,
        "draft": draft,
        "tags": tags,
        # 토픽 클러스터 소속. 내부 링크와 다음 주제 선정이 이 값을 읽습니다.
        "cluster": cluster or "general",
        # 이 글이 답하는 질문. 다음 선정 시 중복 회피에 쓰입니다.
        "question": question or "",
        "ogImage": "../../../../assets/images/placeholder.png",
        "description": description,
        "references": urls[:3] if urls else []
    }
    
    # [E-E-A-T] Last check for author meta
    fm_data['modDatetime'] = seoul_now # Pass datetime object directly
    
    yaml_str = yaml.dump(fm_data, allow_unicode=True, sort_keys=False, indent=2)
    final_markdown = f"---\n{yaml_str}---\n\n{content}"
    
    return final_markdown, prefix, slug



load_dotenv()

if sys.platform == "win32":
    # Ensure terminal can handle UTF-8/Emojis on Windows
    sys.stdout.reconfigure(encoding='utf-8')

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
 
def get_system_status():
    """
    Collects diagnostic information about the current automation state.
    """
    status = {
        "last_run_kst": "정보 없음",
        "headlines_file_exists": False,
        "skipped_reason": None
    }
    
    # Check last_run.txt
    last_run_path = os.path.join("source", "headlines", "last_run.txt")
    if os.path.exists(last_run_path):
        try:
            with open(last_run_path, "r", encoding="utf-8") as f:
                utc_str = f.read().strip()
                utc_dt = datetime.datetime.fromisoformat(utc_str)
                # Convert to KST (+9)
                kst_dt = utc_dt + datetime.timedelta(hours=9)
                status["last_run_kst"] = kst_dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

    # Check today's headlines file
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    headlines_path = os.path.join("source", "headlines", f"{today_str}.txt")
    status["headlines_file_exists"] = os.path.exists(headlines_path)
    
    return status

def print_final_briefing(report):
    """
    Prints a clean, Korean summary and SAVES it to reports/YYYY-MM-DD.txt
    """
    now = datetime.datetime.now()
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    
    filename = now.strftime("%Y-%m-%d.txt")
    filepath = os.path.join(report_dir, filename)

    lines = []
    lines.append("\n" + "="*40)
    lines.append(f"📢 최종 발행 분석 보고서 ({now.strftime('%Y-%m-%d %H:%M:%S')})")
    lines.append("="*40)
    
    # [NEW] 0. System Health & Diagnostics
    lines.append("🛡️ 시스템 상태 및 진단 정보")
    if report.get("system"):
        sys_info = report["system"]
        lines.append(f"- 마지막 뉴스 수집 성공: {sys_info.get('last_run_kst', '알 수 없음')}")
        lines.append(f"- 오늘자 헤드라인 파일: {'✅ 있음' if sys_info.get('headlines_file_exists') else '❌ 없음'}")
        if sys_info.get("skipped_reason"):
            lines.append(f"- ⚠️ 자동화 건너뜀 사유: {sys_info['skipped_reason']}")
    else:
        lines.append("- 시스템 정보 데이터 누락")
    lines.append("-" * 20)
    # 1. Crawling
    if report["crawl"]["success"] is not None:
        if report["crawl"]["success"]:
            lines.append(f"- 🔍 데이터 수집: ✅ 성공 ({report['crawl']['count']}개 URL)")
        else:
            lines.append(f"- 🔍 데이터 수집: ❌ 실패 ({report['crawl']['error']})")
    else:
        lines.append("- 🔍 데이터 수집: ⚪ 건너뜀 (파일 직접 입력 모드)")
        
    # 2. Draft & Detox
    if report["draft"]["success"] is not None:
        if report["draft"]["success"]:
            lines.append(f"- 📑 원고 초안: ✅ 성공 ({report['draft']['path']})")
            if report["draft"].get("warning"):
                lines.append(f"  {report['draft']['warning']}")
            if report["detox"]["success"]:
                lines.append(f"- ✨ 원고 검수: ✅ 완료 (디톡스 필터 적용)")
            else:
                lines.append(f"- ✨ 원고 검수: ⚠️ 건너뜀 또는 실패 ({report['detox']['error']})")

            verdict = report["detox"].get("fact_verdict")
            if verdict == "pass":
                lines.append("- 🔬 사실 검증: ✅ 통과 (모든 수치가 소스에서 확인됨)")
            elif verdict == "revised":
                lines.append("- 🔬 사실 검증: 🔧 교정 후 통과")
            elif verdict == "hold":
                lines.append("- 🔬 사실 검증: 🛑 보류 (draft:true 로 저장, 수동 확인 필요)")
        else:
            err = report["draft"].get("error") or ""
            if err.startswith("[중단]"):
                lines.append(f"- 📑 원고 초안: 🛑 발행 중단 — {err[4:].strip()}")
                lines.append("  (소스로 답할 수 없는 주제였습니다. 나쁜 글을 쓰지 않은 것은 정상 동작입니다)")
            else:
                lines.append("- 📑 원고 초안: ❌ 실패")
    else:
        lines.append("- 📑 원고 초안/검수: ⚪ 건너뜀 (기존 파일 사용)")

    # 3. Images
    if report["images"].get("diagrams"):
        lines.append(f"- 📐 도해 렌더링: ✅ {report['images']['diagrams']}건 (API 비용 0)")

    if report["images"]["requested"] > 0:
        status = "✅ 완수" if report["images"]["success"] == report["images"]["requested"] else "⚠️ 부분 성공"
        lines.append(f"- 🖼️ 이미지 생성: {status} ({report['images']['success']} / {report['images']['requested']} 완료)")
        if report["images"].get("error"):
            lines.append(f"  ❌ 에러 발생: {report['images']['error']}")
    elif report["images"]["success"] is None:
         lines.append("- 🖼️ 이미지 생성: ⚪ 건너뜀")
    else:
        lines.append("- 🖼️ 이미지 생성: ⚪ 없음 (플레이스홀더 미발견)")

    # 4. Translations
    lines.append("- 🌐 다국어 번역 상태:")
    if not report.get("translations"):
        lines.append("  - (번역 단계가 실행되지 않았습니다)")
    else:
        for lang, res in report["translations"].items():
            status = "✅ 성공" if res["success"] else f"❌ 실패 (사유: {res['error']})"
            lines.append(f"  - {lang.upper()}: {status}")

    lines.append("="*40)
    if any(not res["success"] for res in report["translations"].values()):
        lines.append("💡 실패한 번역이 있다면 API 부하일 가능성이 높습니다. 잠시 후 다시 시도해 보세요.")
    lines.append("="*40 + "\n")

    # [NEW] 비용/토큰 메트릭 추적
    metrics = gemini_tracker.get_summary_and_cost()
    lines.append("\n" + "="*40)
    lines.append("💰 이번 세션 리소스 사용량")
    lines.append("="*40)
    lines.append(f"- 텍스트 프롬프트: {metrics['prompt']:,} tokens")
    lines.append(f"- 결과 생성: {metrics['candidate']:,} tokens")
    if metrics['images'] > 0:
        lines.append(f"- AI 이미지 생성: {metrics['images']} 회")
    lines.append(f"- 💵 추정 비용: ${metrics['cost_usd']:.4f} USD")
    lines.append("="*40 + "\n")

    # Output to Console
    final_output = "\n".join(lines)
    print(final_output)

    # Save to File
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(final_output + "\n\n")
        print(f"💾 보고서가 파일로 저장되었습니다: {filepath}")
    except Exception as e:
        print(f"⚠️ 보고서 파일 저장 중 오류 발생: {e}")

def process_single_file(file_path, folder="posts", target_lang=None, schedule_type=None):
    """
    Bypass crawl/gen/review and only run translation for an existing .md file.
    """
    print(f"\n[RE-RUN] File translation mode detected.")
    print(f"Source file: {file_path}")
    print(f"Category: {folder}")
    if target_lang:
        print(f"Target language: {target_lang}")

    report = {
        "crawl": {"success": None, "count": 0, "error": None},
        "draft": {"success": None, "path": None, "warning": None},
        "detox": {"success": None, "error": None},
        "images": {"success": None, "requested": 0},
        "translations": {}
    }

    if not os.path.exists(file_path):
        report["draft"] = {"success": False, "error": f"File not found: {file_path}"}
        print_final_briefing(report)
        return

    with open(file_path, "r", encoding="utf-8") as f:
        draft = f.read()

    # Localize existing English alt tags in the draft
    # Find all ![Alt](Path) where Alt is in English
    alt_regex = re.compile(r'!\[(.*?)\]\((.*?)\)')
    matches = alt_regex.findall(draft)
    for alt, path in matches:
        # Check if alt contains English letters (simple check)
        if re.search(r'[a-zA-Z]', alt):
            print(f"Localizing alt tag: {alt[:30]}...")
            localized_alt = translate_text(alt, "ko")
            draft = draft.replace(f"![{alt}]({path})", f"![{localized_alt}]({path})")
            
    # Save the updated Korean draft
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(draft)

    slug_raw = os.path.splitext(os.path.basename(file_path))[0]
    # Remove YYMMDD_ prefix if it exists to avoid double prefixes during translation
    slug = slug_raw[7:] if re.match(r'^\d{6}_', slug_raw) else slug_raw

    # Run Translation
    print(f"\n=== Translating to requested languages ===")
    target_langs = [target_lang] if target_lang else None
    results = translate_and_save(draft, slug, folder, target_langs=target_langs)
    report["translations"] = results

    # Optional Push
    if DRY_RUN:
        print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
    else:
        # 무인 자동화를 위해 질문 없이 바로 진행 (y로 간주)
        print(f"\n🚀 모든 작업 완료. '{slug}' 포스트를 GitHub에 자동으로 연동(Push)합니다.")
        push_to_github(f"Re-translate post: {slug} ({target_lang if target_lang else 'all'})")

    print_final_briefing(report)

def process_urls(keyword=None, folder="posts", urls=None, schedule_type=None,
                 lesson_ctx=None):
    """
    Main pipeline: (Crawl) -> Generate -> Review -> Image Gen -> Translate -> (Push)
    If 'urls' is provided as a list, it bypasses keyword-based file loading.
    """
    report = {
        "system": get_system_status(), # 초기화 시 시스템 정보 수집
        "crawl": {"success": False, "count": 0, "error": None},
        "draft": {"success": False, "path": None, "warning": None, "error": None},
        "detox": {"success": False, "error": None},
        "images": {"success": 0, "requested": 0, "error": None},
        "translations": {}
    }

    # 1. Determine URL source
    if urls and isinstance(urls, list):
        print(f"Using {len(urls)} provided URLs for generation.")
        print(f"Category: {folder}")
        if keyword:
            print(f"Topic: {keyword}")
    elif keyword:
        keyword_file = os.path.join("source", "url", f"{keyword}.txt")
        if not os.path.exists(keyword_file):
            report["crawl"]["error"] = f"Keyword file not found: {keyword_file}"
            print_final_briefing(report)
            return
        with open(keyword_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        print(f"Category: {folder}")
        print(f"Targeting keyword source: {keyword}")
    else:
        # Fallback to urls.txt
        if not os.path.exists("urls.txt"):
            report["crawl"]["error"] = "urls.txt not found"
            print_final_briefing(report)
            return
        with open("urls.txt", "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        print("No keyword provided. Using fallback urls.txt")

    # 2. Crawl
    print(f"\n=== Found {len(urls)} URLs to crawl ===")
    all_content = []
    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Crawling: {url}")
        content = fetch_content(url)
        if content and content['body']:
            all_content.append(content)
            print(f"  [PASS] Got {len(content['body'])} characters")
        else:
            print(f"  [FAIL] Skipped (no content)")

    if not all_content:
        report["crawl"]["error"] = "No content could be fetched"
        print_final_briefing(report)
        return
    
    report["crawl"]["success"] = True
    report["crawl"]["count"] = len(all_content)

    # 3. Generate initial draft parts
    combined_body = "\n\n---\n\n".join([c['body'] for c in all_content])
    print(f"\n=== Combined {len(all_content)} pages into {len(combined_body)} chars ===")
    
    # [수리] '날카로운 비판적 스탠스' 생성 단계를 제거했습니다.
    # 이 단계가 모든 글을 비평 칼럼으로 만들었고, 그 결과 발행된 글들이
    # 전부 "혁신인가 함정인가 / ~의 역설" 형태로 수렴했습니다.
    # 정보성 문서에는 논조가 필요 없습니다.

    print(f"\nGenerating draft with Gemini ({folder} mode)...")
    crawled_summary = {
        "title": all_content[0].get('title', 'Untitled Issue'),
        "url": urls[0],
        "body": combined_body[:30000] # Limit to avoid token issues
    }

    draft_data, gen_info = generate_blog_post(
        crawled_summary, folder=folder, keyword=keyword, schedule_type=schedule_type,
        lesson_ctx=lesson_ctx
    )

    # [수리] 중단 경로. 소스로 답할 수 없으면 발행하지 않습니다.
    # 기존 파이프라인에는 "쓸 수 없음"이라는 결과가 없어서 소스가 부실해도 한 편을 뱉었습니다.
    if not draft_data:
        reason = gen_info.get("reason", "알 수 없는 사유")
        print(f"\n🛑 발행 중단: {reason}")
        report["draft"]["error"] = f"[중단] {reason}"
        report["system"]["skipped_reason"] = reason
        print_final_briefing(report)
        return

    source_text = gen_info.get("source_text", combined_body)
    if gen_info.get("conflicts"):
        report["draft"]["warning"] = f"소스 간 상충 {len(gen_info['conflicts'])}건 (본문에 명시됨)"

    # 3.5 Stage 3.5: Manuscript Inspection (Detox)
    # [수리] 기존에는 `if folder != "posts"` 조건 때문에 블로그 포스트가 이 단계를
    #       한 번도 통과하지 않았습니다. 그런데도 report["detox"]["success"] = True 를
    #       박아넣어 매 실행 "원고 검수 완료"라고 보고했습니다.
    #       이 저장소에서 가장 잘 작성된 품질 필터가 5개월간 꺼져 있던 원인입니다.
    print(f"\n=== Stage 3.5: Manuscript Inspection (Detox) ===")
    max_retries = 3
    reviewed_data = None
    for attempt in range(max_retries):
        print(f"  [Attempt {attempt+1}/{max_retries}] Starting detox...")
        reviewed_data = review_manuscript(draft_data, folder=folder)
        if reviewed_data and reviewed_data != draft_data:
            report["detox"]["success"] = True
            print(f"  ✅ Detox successful.")
            break
        else:
            print(f"  ⚠️ Detox attempt {attempt+1} failed or returned no changes.")
            if attempt < max_retries - 1:
                time.sleep(5) # Wait before retry

    if not report["detox"]["success"]:
        report["detox"]["error"] = "Detox failed after all retries, keeping original parts"
        print(f"  ❌ All detox attempts failed. Using original parts.")
        reviewed_data = draft_data

    # 3.6 Stage 3.6: Fact Gate
    # [신설] 원고의 수치 주장을 소스 원문과 대조합니다.
    #        미검증 수치는 교정하고, 교정 후에도 남으면 draft:true 로 보류합니다.
    verified_content, verdict, fact_report = verifier.verify(reviewed_data['content'], source_text)
    reviewed_data['content'] = verified_content
    hold_for_review = (verdict == "hold")

    report["detox"]["fact_verdict"] = verdict
    if verdict == "revised":
        report["draft"]["warning"] = f"미검증 수치 {len(fact_report['before'])}건 교정됨"
    elif verdict == "hold":
        report["draft"]["warning"] = (
            f"⚠️ 미검증 수치 {len(fact_report['after'])}건이 남아 draft:true 로 보류합니다. "
            f"수동 확인 후 draft 를 false 로 바꾸세요."
        )

    # NEW STEP: Stage 3.7: Metadata Assembly & Slug Generation
    print(f"\n=== Stage 3.7: Metadata Assembly & Slug Generation ===")
    draft, prefix, slug = assemble_post_metadata(
        reviewed_data, folder=folder, keyword=keyword, urls=urls, draft=hold_for_review,
        cluster=(lesson_ctx or {}).get("lesson_id"), question=(lesson_ctx or {}).get("goal")
    )
    print(f"  ✅ Metadata assembled. Final Slug: {slug}")

    # [폐지] Stage 3.7.5 Auto Glossary Extraction
    # 포스트 한 편마다 용어사전 한 편을 자동 생성하고 4개 언어로 번역했습니다.
    # 그 결과 포스트 118편에 용어사전 109편이 쌓여 콘텐츠의 절반이 자동 생성
    # 사전 항목이 됐고, 본문에는 실제로 존재하지 않는 용어사전을 가리키는
    # 툴팁 링크가 43개 박혔습니다. 용어사전 게시판과 함께 전면 폐지합니다.

    # 3.7.8 Inject Internal Links (SEO)
    print(f"\n=== Stage 3.7.8: Internal Linking ===")
    draft = inject_internal_links(draft, folder, lesson_ctx=lesson_ctx)

    # 3.9 Stage 3.9: 도해 렌더링 (결정론적, API 호출 없음)
    # [신설] 구조가 있는 내용은 생성 이미지가 아니라 HTML/CSS 도해로 표현합니다.
    #        생성 모델은 도해 안의 글자를 정확히 그리지 못하고, 장당 과금되며,
    #        번역판에서 이미지 속 영어 텍스트가 그대로 남습니다.
    print(f"\n=== Stage 3.9: 도해 렌더링 ===")
    draft, dgm_count, dgm_dropped = diagram.replace_placeholders(draft)
    if dgm_count:
        print(f"  ✅ 도해 {dgm_count}건 렌더링 (비용 0)")
    else:
        print("  · 도해 없음")
    for spec in dgm_dropped:
        print(f"  ⚠️ 해석할 수 없는 도해 표기를 제거했습니다: {spec[:80]}")
    report["images"]["diagrams"] = dgm_count

    # 4. Process Images
    # 신 파이프라인은 [이미지:] 를 생성하지 않습니다. 이 경로는 기존 파일 재작업
    # (process_single_file) 및 레거시 원고 호환용으로만 남겨 둡니다.
    image_pattern = re.compile(r'(?:\*\*|\_)?!*\\?\[\s*이미지\s*:\s*([^\]\\]+)\\?\](?:\*\*|\_)?|(?:\*\*|\_)?!*\[이미지\]\(([^)]+)\)(?:\*\*|\_)?')
    image_matches = list(image_pattern.finditer(draft))
    
    source_folder_name = keyword if keyword else "general"
    source_folder_name = re.sub(r'[\s\\/:*?"<>|]+', '_', source_folder_name).strip('_')
    
    source_img_dir = os.path.join("source", folder, source_folder_name)
    os.makedirs(source_img_dir, exist_ok=True)
    
    print(f"Found {len(image_matches)} image placeholders.")
    report["images"]["requested"] = len(image_matches)

    image_context = f"Post Title: {reviewed_data['title']} | Keyword: {keyword if keyword else 'Technology'}"

    for i, match in enumerate(image_matches):
        prompt = (match.group(1) or match.group(2)).strip()
        full_match_str = match.group(0)
        
        img_uuid = str(uuid.uuid4())[:8]
        img_filename = f"{img_uuid}-{i}.webp"
        img_path = os.path.join(source_img_dir, img_filename)
        
        print(f"Generating AI image for: {prompt[:50]}...")
        generated_path, img_error = generate_image(prompt, img_path, context=image_context)
        
        if generated_path:
            report["images"]["success"] += 1
            rel_path = f"../../../../../source/{folder}/{source_folder_name}/{img_uuid}-{i}.webp"
            # Markdown link fix: encode parentheses in path
            encoded_rel_path = rel_path.replace('(', '%28').replace(')', '%29')
            
            alt_clean_prompt = f"다음 이미지 생성용 프롬프트에서 시각적 스타일 키워드(4k, 해상도 등)를 제외하고, 초보자도 이해할 수 있는 핵심 의미만 한 문장으로 요약해서 ko로 번역해줘:\n{prompt}"
            translated_alt = translate_text(alt_clean_prompt, "ko")
            alt_keyword = keyword if keyword else "IT 트렌드"
            md_img_link = f"![{alt_keyword} - {translated_alt}]({encoded_rel_path})"
            
            # 직접 치환 (마크다운 ** 등 스타일 태그 포함 매칭되었으므로 그대로 치환하여 제거)
            draft = draft.replace(full_match_str, md_img_link)
            
            if i == 0:
                # 첫 번째 이미지를 ogImage로 자동 설정
                draft = re.sub(r'ogImage:.*', f'ogImage: "{rel_path}"', draft)
        else:
            report["images"]["error"] = img_error if img_error else "Unknown Error"

    # AI가 생성 과정에서 [이미지: ...]를 <p> 태그로 감싸버린 경우 마크다운 파서가 이미지를 렌더링하지 못하므로, 이를 제거합니다.
    # MDX 파서가 정상적으로 인식할 수 있도록 위아래로 빈 줄(\n\n)을 추가합니다.
    draft = re.sub(r'<p>\s*(!\[.*?\]\(.*?\))\s*</p>', r'\n\n\1\n\n', draft)

    # 5. Save the final draft
    target_dir = os.path.join("src", "data", "blog", "ko", folder)
    os.makedirs(target_dir, exist_ok=True)
    post_path = os.path.join(target_dir, f"{prefix}{slug}.md")
    
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(draft)
    
    print(f"\n[DONE] Successfully saved Korean blog post to {post_path}!")
    report["draft"]["success"] = True
    report["draft"]["path"] = post_path
    
    # 6. Translate to EN, CN, JP
    print(f"\n=== Translating to 3 languages ===")
    results = translate_and_save(draft, slug, folder)
    report["translations"] = results
    
    # 7. Push to GitHub (REMOVED)
    # GitHub Actions workflow now handles `pnpm build` first, and if successful, runs `publish.py`
    print(f"\n🚀 파일 생성 완료. (자동 푸시는 이제 GitHub Actions의 빌드 검증 이후에 수행됩니다.)")
        
    # 🚨 FINAL BRIEFING
    print_final_briefing(report)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Blog Automation Pipeline")
    
    # Support positional arguments (for the requested format: python main.py keyword folder)
    parser.add_argument("p_input_arg", nargs="?", help="Keyword or Path to .md file")
    parser.add_argument("p_folder", nargs="?", help="Target folder (default: posts)")
    parser.add_argument("p_target_lang", nargs="?", help="Specific language for retry mode (en, cn, jp)")
    
    # Support named arguments for clarity
    parser.add_argument("--keyword", help="Target keyword")
    parser.add_argument("--folder", help="Target folder")
    parser.add_argument("--lang", help="Target language")
    parser.add_argument("--schedule", help="스케줄 라벨 (리포트 표기용)")
    parser.add_argument("--lesson", help="특정 레슨을 지정 (curriculum.yaml 의 id)")

    args = parser.parse_args()

    # Priorities: Named arguments > Positional arguments > Defaults
    input_arg = args.keyword if args.keyword else args.p_input_arg
    folder = args.folder if args.folder else (args.p_folder if args.p_folder else "posts")
    target_lang = args.lang if args.lang else args.p_target_lang
    
    if input_arg and input_arg.endswith(".md"):
        # 기존 파일 재작업 모드
        process_single_file(input_arg, folder, target_lang, schedule_type=args.schedule)

    elif input_arg:
        # 🚀 [MANUAL MODE] 수동 키워드 입력 시 DeepSearch 연동
        print(f"\n🚀 [MANUAL MODE] Keyword provided: {input_arg}")
        print("Starting DeepSearch & Filter for manual keyword...")
        
        # 웹 검색 및 10개 선별 수행
        top_urls = deep_search_and_filter(input_arg, num_results=100)
        
        if top_urls:
            # 수동 모드 역사 기록
            save_keyword_to_history(input_arg, "수동선정")
            process_urls(urls=top_urls, keyword=input_arg, folder=folder, schedule_type=args.schedule)
        else:
            print(f"❌ '{input_arg}'에 대한 검색 결과에서 유효한 소스를 찾지 못했습니다.")
    else:
        # 🔥 완전 자동 모드 (파일 생성 -> 분석 -> 포스팅)
        print("\n🚀 [AUTO MODE] No arguments provided. Starting full automation pipeline...")
        
        master_report = {
            "system": get_system_status(),
            "crawl": {"success": None, "count": 0, "error": None},
            "draft": {"success": None, "path": None, "warning": None},
            "detox": {"success": None, "error": None},
            "images": {"success": None, "requested": 0},
            "translations": {}
        }
        
        try:
            # 1. 선생 에이전트가 다음 레슨을 정합니다.
            #    선수 지식이 모두 발행된 레슨 중에서만 고릅니다.
            cur = teacher.load_curriculum()
            problems = teacher.validate_curriculum(cur)
            if problems:
                for pr in problems:
                    print(f"❌ 커리큘럼 문제: {pr}")
                master_report["system"]["skipped_reason"] = "커리큘럼 구조 오류"
                sys.exit(1)

            teacher.print_status(cur)
            lesson, lesson_ctx = teacher.next_lesson(cur, force_id=args.lesson)
            if lesson is None:
                print(f"🛑 {lesson_ctx}")
                master_report["system"]["skipped_reason"] = str(lesson_ctx)
                sys.exit(0)

            print(f"\n🎓 오늘의 레슨: [{lesson_ctx['track_name']}] {lesson['id']}")
            print(f"   목표: {lesson_ctx['goal']}")
            print(f"   새 용어: {', '.join(lesson_ctx['teaches']) or '없음'}")

            save_keyword_to_history(lesson_ctx["goal"], f"lesson:{lesson['id']}")

            # 2. 참고 자료를 모읍니다.
            #    개념 설명 자체는 소스가 없어도 되지만, 도구 이름·명령어·용어의
            #    established 정의처럼 '틀리면 독자가 막히는 사실'은 소스로 확인해야
            #    합니다. (소스 없이 생성했더니 '바이브코딩'의 정의를 지어냈습니다)
            search_query = " ".join(lesson_ctx["teaches"][:3]) or lesson_ctx["goal"]
            print(f"\n🔍 참고 자료 검색: {search_query}")
            top_urls = deep_search_and_filter(search_query, num_results=60)

            if not top_urls:
                print("⚠️ 참고 자료를 찾지 못했습니다. 모델 지식만으로 집필합니다.")
                master_report["system"]["skipped_reason"] = "참고 자료 없음 (모델 지식만 사용)"

            process_urls(
                urls=top_urls or [],
                keyword=search_query,
                folder=folder,
                schedule_type="lesson",
                lesson_ctx=lesson_ctx,
            )
            sys.exit(0)
        except SystemExit:
            # sys.exit() 호출 시에도 finally 블록이 실행되도록 함
            pass
        except Exception as e:
            error_msg = f"자동화 중 치명적 오류 발생: {str(e)}"
            print(f"❌ {error_msg}")
            master_report["system"]["skipped_reason"] = error_msg
        finally:
            # 리포트 출력 및 저장
            # 만약 process_urls 내에서 이미 리포트가 생성되었다면 중복될 수 있으나, 
            # 에러 발생 시에는 여기서 생성하는 것이 안전함.
            # 중복 방지를 위해 파일 존재 여부나 상태를 체크할 수도 있으나 우선은 단순 출력.
            print_final_briefing(master_report)
            
            # 실패 시 리포트는 로컬에만 저장하고, healer.py가 이후에 처리하도록 맡김
            print("\n❌ Automation pipeline failed. Generating diagnostic report locally...")
