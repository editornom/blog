import os
import sys
import uuid
import re
import time
import datetime
from dotenv import load_dotenv
from urllib.parse import urlparse
import yaml

from crawler import fetch_content, extract_related_links
from generator import generate_blog_post
from reviewer import review_manuscript
from imagen_helper import generate_image
from translator import translate_and_save, translate_text
from publish import push_to_github
from accordian import load_faq_content, prepare_faq_data
from headline_crawler import generate_daily_headlines_file
from trend_catcher import get_daily_topic_from_file, save_keyword_to_history
from search_expert import deep_search_and_filter
from faq_expert import generate_faq
from api_utils import gemini_tracker
from glossary_expert import pick_daily_glossary_keyword
from google import genai

def assemble_post_metadata(reviewed_data, folder="posts", keyword="", urls=None):
    """
    Creates final Frontmatter and combines it with refined content.
    Generates SEO-friendly slug and description based on REFINED content.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    title = reviewed_data['title']
    content = reviewed_data['content']
    
    # 1. Generate SEO-optimized Slug from REFINED Title
    print(f"  [Assembler] Generating optimized slug...")
    slug_prompt = f"Create a short, SEO-friendly English URL slug from this blog title: '{title}'. Output ONLY the slug (lowercase-and-hyphens-only)."
    slug_resp = client.models.generate_content(model='models/gemini-3-flash-preview', contents=slug_prompt)
    slug = slug_resp.text.strip().lower().replace(' ', '-').replace('"', '').replace("'", "")
    # Remove any non-alphanumeric/hyphen chars just in case
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    
    # 2. Generate Description from REFINED Content
    print(f"  [Assembler] Generating meta description...")
    desc_prompt = f"Summarize this blog post into 1-2 professional sentences for a meta description (SEO): \n\n{content[:1000]}"
    desc_resp = client.models.generate_content(model='models/gemini-3-flash-preview', contents=desc_prompt)
    description = desc_resp.text.strip().replace('"', "'")
    
    # 3. Time calculation
    seoul_tz = datetime.timezone(datetime.timedelta(hours=9))
    seoul_now = datetime.datetime.now(seoul_tz)
    pub_time = seoul_now - datetime.timedelta(minutes=10) # Buffer
    prefix = pub_time.strftime("%y%m%d_")
    
    # 4. Assemble YAML
    fm_data = {
        "title": title,
        "author": "editornom",
        "author_role": "Senior Tech Editor",
        "author_url": "https://editornom.com/about",
        "pubDatetime": pub_time, # Pass datetime object directly
        "slug": slug,
        "featured": False,
        "draft": False,
        "ogImage": "../../../../assets/images/placeholder.png",
        "description": description,
        "references": urls[:10] if urls else []
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
        else:
            lines.append("- 📑 원고 초안: ❌ 실패")
    else:
        lines.append("- 📑 원고 초안/검수: ⚪ 건너뜀 (기존 파일 사용)")

    # 3. Images
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

def process_single_file(file_path, folder="posts", target_lang=None, include_faq=False):
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

    slug = os.path.splitext(os.path.basename(file_path))[0]

    # Add FAQ if requested (using slug as keyword)
    if include_faq:
        # Try finding FAQ by slug first, then fallback to parts of slug or manual check
        # For TurboQuant, slug is 'google-turboquant-ai-efficiency-impact'
        # But file is '터보퀀트.txt'
        # mapping or manual input.
        if "turboquant" in slug.lower():
            keyword = "터보퀀트"
        elif "gemma-4" in slug.lower():
            keyword = "구글젬마4"
        elif "utm" in slug.lower():
            keyword = "UTM"
        elif "colocation" in slug.lower():
            keyword = "코로케이션"
        elif "llm-wiki" in slug.lower():
            keyword = "llmwiki"
        else:
            keyword = slug
        
        faqs = load_faq_content(keyword)
        if faqs:
            # First, strip existing legacy FAQ in body if any to avoid duplicates
            if "## ✅ 자주 묻는 질문 (FAQ)" in draft:
                draft = draft.split("## ✅ 자주 묻는 질문 (FAQ)")[0].strip()
            
            # Use prepare_faq_data to cleanup draft and get faq list
            draft, faqs = prepare_faq_data(draft, faqs)
            
            # NOTE: For frontmatter insertion, we'll need a more robust check. 
            # If the draft already has 'faqs:' in frontmatter, we might want to skip or update.
            # For simplicity in this 'posts' mode, we trust the translator to handle frontmatter if it's there,
            # or we manually inject if missing.
            # [E-E-A-T] Update metadata for freshness and authority
            parts = draft.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1])
                if include_faq and faqs:
                    fm['faqs'] = faqs
                
                fm['modDatetime'] = datetime.datetime.now().astimezone()
                fm['author_role'] = "Senior Tech Editor"
                fm['author_url'] = "https://editornom.com/about"
                
                new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
                draft = f"---\n{new_fm}---\n{parts[2].strip()}"
            
            print(f"Ensured FAQ data for '{keyword}' is ready for translation.")
            
            # Save the updated Korean draft
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(draft)
        else:
            print(f"Warning: FAQ content not found for {keyword}")
    
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

def process_urls(keyword=None, folder="posts", include_faq=False, urls=None):
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
    
    print(f"Generating draft parts with Gemini ({folder} mode)...")
    crawled_summary = {
        "title": all_content[0].get('title', 'Untitled Issue'),
        "url": urls[0],
        "body": combined_body[:30000] # Limit to avoid token issues
    }
    
    draft_data, density_warning = generate_blog_post(crawled_summary, folder=folder, keyword=keyword)
    if not draft_data:
        print("Error: Failed to generate initial blog post parts.")
        report["draft"]["error"] = "Failed to generate initial blog post parts."
        print_final_briefing(report)
        return
    
    if density_warning:
        report["draft"]["warning"] = density_warning
    
    # 3.5 Stage 3.5: Manuscript Inspection (Detox)
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

    # NEW STEP: Stage 3.7: Metadata Assembly & Slug Generation
    print(f"\n=== Stage 3.7: Metadata Assembly & Slug Generation ===")
    draft, prefix, slug = assemble_post_metadata(reviewed_data, folder=folder, keyword=keyword, urls=urls)
    print(f"  ✅ Metadata assembled. Final Slug: {slug}")

    # 3.8 Add FAQ if requested (New YAML Frontmatter Architecture)
    if include_faq and keyword:
        generate_faq(draft, keyword)
        faqs = load_faq_content(keyword)
        if faqs:
            # 본문의 레거시 FAQ 태그 제거 및 데이터 확보
            draft, faqs_data = prepare_faq_data(draft, faqs)
            
            # 프런트매터 영역에 YAML 배열 형태로 주입
            faq_yaml = yaml.dump({"faqs": faqs_data}, allow_unicode=True, sort_keys=False, indent=2)
            faq_yaml = faq_yaml.replace("---", "").strip()
            
            # Insert before the last Frontmatter separator
            draft = re.sub(r'\n---', f'\n{faq_yaml}\n---', draft, count=1, flags=re.MULTILINE)
            print(f"✅ Injected {len(faqs)} FAQ items into YAML Frontmatter.")
        else:
            print(f"Warning: FAQ file not found or empty for keyword '{keyword}'")

    # 4. Process Images
    image_placeholders = re.findall(r'(?:!\[이미지\]\(|\[이미지: )(.*?)(?:\)|\])', draft)
    
    source_folder_name = keyword if keyword else "general"
    source_folder_name = re.sub(r'[\s\\/:*?"<>|]+', '_', source_folder_name).strip('_')
    
    source_img_dir = os.path.join("source", folder, source_folder_name)
    os.makedirs(source_img_dir, exist_ok=True)
    
    print(f"Found {len(image_placeholders)} image placeholders.")
    report["images"]["requested"] = len(image_placeholders)

    image_context = f"Post Title: {reviewed_data['title']} | Keyword: {keyword if keyword else 'Technology'}"

    for i, prompt in enumerate(image_placeholders):
        img_uuid = str(uuid.uuid4())[:8]
        img_filename = f"{img_uuid}-{i}.webp"
        img_path = os.path.join(source_img_dir, img_filename)
        
        print(f"Generating AI image for: {prompt[:50]}...")
        generated_path, img_error = generate_image(prompt, img_path, context=image_context)
        
        if generated_path:
            report["images"]["success"] += 1
            rel_path = f"../../../../../source/{folder}/{source_folder_name}/{img_uuid}-{i}.webp"
            
            alt_clean_prompt = f"다음 이미지 생성용 프롬프트에서 시각적 스타일 키워드(4k, 해상도 등)를 제외하고, 초보자도 이해할 수 있는 핵심 의미만 한 문장으로 요약해서 ko로 번역해줘:\n{prompt}"
            translated_alt = translate_text(alt_clean_prompt, "ko")
            alt_keyword = keyword if keyword else "IT 트렌드"
            md_img_link = f"![{alt_keyword} - {translated_alt}]({rel_path})"
            
            draft = draft.replace(f"[이미지: {prompt}]", md_img_link)
            draft = draft.replace(f"![이미지]({prompt})", md_img_link)
            
            if i == 0:
                draft = re.sub(r'ogImage: ".*?"', f'ogImage: "{rel_path}"', draft)
        else:
            report["images"]["error"] = img_error if img_error else "Unknown Error"

    # [NEW] E-E-A-T 신뢰도 확보를 위한 참고 문헌 (아코디언 UI로 숨김 처리)
    if urls:
        references_html = "\n\n---\n\n<details>\n<summary>📚 참고 자료 확인하기</summary>\n<ul>\n"
        for u in urls[:10]: # Too many links can be spammy, limit to 10
            domain = urlparse(u).netloc.replace("www.", "")
            references_html += f"<li><a href=\"{u}\" target=\"_blank\" rel=\"noopener noreferrer\">{domain} 원문</a></li>\n"
        references_html += "</ul>\n</details>\n"
        draft += references_html

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
    
    # 7. Push to GitHub
    if DRY_RUN:
        print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
    else:
        # 무인 자동화를 위해 질문 없이 바로 진행 (y로 간주)
        print(f"\n🚀 모든 작업 완료. '{slug}' 포스트를 GitHub에 자동으로 연동(Push)합니다.")
        from publish import push_to_github
        success = push_to_github(f"Auto-generate post: {slug}")
        if not success:
            print("❌ GitHub Push에 실패했습니다.")
            sys.exit(1)
        
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
    parser.add_argument("--auto-glossary", action="store_true", help="Automated glossary generation mode")

    args = parser.parse_args()

    # Priorities: Named arguments > Positional arguments > Defaults
    input_arg = args.keyword if args.keyword else args.p_input_arg
    folder = args.folder if args.folder else (args.p_folder if args.p_folder else "posts")
    target_lang = args.lang if args.lang else args.p_target_lang
    
    # 🚀 [New] 자동 용어 사전 모드 지원
    if args.auto_glossary:
        print("\n📚 [AUTO GLOSSARY MODE] Selecting a new technical term...")
        auto_term = pick_daily_glossary_keyword()
        if auto_term:
            input_arg = auto_term
            folder = "glossary"
            print(f"✨ Selected Keyword: {input_arg}")
        else:
            print("❌ Failed to select a glossary term. Aborting.")
            sys.exit(1)

    # 🚀 무인 자동화 모드: 질문 없이 FAQ 생성 및 삽입을 기본값으로 설정
    include_faq = True
    print("\n✅ FAQ 자동 생성 모드가 활성화되었습니다.")
    
    if input_arg and input_arg.endswith(".md"):
        # 기존 파일 재작업 모드
        process_single_file(input_arg, folder, target_lang, include_faq=include_faq)

    elif input_arg:
        # 🚀 [MANUAL MODE] 수동 키워드 입력 시 DeepSearch 연동
        print(f"\n🚀 [MANUAL MODE] Keyword provided: {input_arg}")
        print("Starting DeepSearch & Filter for manual keyword...")
        
        # 웹 검색 및 10개 선별 수행
        top_urls = deep_search_and_filter(input_arg, num_results=100)
        
        if top_urls:
            # 수동 모드 역사 기록
            save_keyword_to_history(input_arg, "수동선정")
            process_urls(urls=top_urls, keyword=input_arg, folder=folder, include_faq=include_faq)
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
            # 1. 크롤러 실행: list.txt 읽어서 YYYYMMDD.txt 생성
            daily_file = generate_daily_headlines_file("list.txt")
            master_report["system"]["headlines_file_exists"] = os.path.exists(daily_file) if daily_file else False
            
            auto_keyword = None
            if daily_file:
                # 2. 트렌드 캐처 실행: 수집된 파일 읽어서 키워드 도출
                auto_keyword = get_daily_topic_from_file(daily_file)
            
            if not auto_keyword:
                # 헤드라인 수집이 아예 안 됐거나, 키워드 추출 중 오류 발생 시 에버그린 fallback
                print("⚠️ 헤드라인 기반 키워드 도출에 실패(또는 기사 없음). 즉시 Evergreen 키워드(Fallback) 모드로 전환합니다.")
                master_report["system"]["skipped_reason"] = "헤드라인 수집 실패 또는 새로운 기사 없음 (에버그린 폴백 진행)"
                from trend_catcher import get_evergreen_keywords, save_keyword_to_history
                import random
                
                evergreen_pool = get_evergreen_keywords()
                if evergreen_pool:
                    auto_keyword = random.choice(evergreen_pool)
                    print(f"🔄 대비책(Fallback) 가동: 상시 키워드 풀에서 '{auto_keyword}'(을)를 선택합니다.")
                    save_keyword_to_history(auto_keyword, "Fallback_Auto_Pipeline")
                else:
                    error_msg = "상시 키워드 목록도 비어있어 파이프라인을 중단합니다."
                    print(f"❌ {error_msg}")
                    master_report["system"]["skipped_reason"] = error_msg
                    sys.exit(1)
                    
            print(f"✨ Auto-selected Keyword: {auto_keyword}")
            
            # 🚀 [New Pipeline] DeepSearch & Filter
            top_urls = deep_search_and_filter(auto_keyword, num_results=100)
            
            # 검색 실패 시 한 번 더 에버그린 풀에서 다른 단어로 시도
            if not top_urls:
                print(f"⚠️ '{auto_keyword}'에 대한 검색 결과가 빈약합니다. Evergreen 키워드로 2차 재시도합니다.")
                master_report["system"]["skipped_reason"] = f"'{auto_keyword}' 검색 결과 부족 (2차 폴백 진행)"
                from trend_catcher import get_evergreen_keywords, save_keyword_to_history
                import random
                evergreen_pool = get_evergreen_keywords()
                if auto_keyword in evergreen_pool:
                    evergreen_pool.remove(auto_keyword)
                if evergreen_pool:
                    auto_keyword = random.choice(evergreen_pool)
                    print(f"🔄 2차 대비책(Fallback) 가동: '{auto_keyword}'(을)를 선택합니다.")
                    save_keyword_to_history(auto_keyword, "Fallback_DeepSearchFail")
                    top_urls = deep_search_and_filter(auto_keyword, num_results=100)

            if top_urls:
                # 3. 선별된 고품질 URL들을 사용하여 포스팅 작성
                process_urls(urls=top_urls, keyword=auto_keyword, folder=folder, include_faq=include_faq)
                # process_urls 내부에서 print_final_briefing을 호출하므로 여기서는 중복 호출하지 않기 위해 
                # master_report를 직접 관리하는 방식 대신 process_urls의 결과를 받거나 
                # 혹은 전역적인 상태 관리가 필요함. 
                # 여기서는 단순화를 위해 process_urls가 끝난 후 return 하도록 함.
                sys.exit(0) 
            else:
                error_msg = "검색 결과에서 유효한 소스를 끝내 찾지 못하여 파이프라인을 중단합니다."
                print(f"❌ {error_msg}")
                master_report["system"]["skipped_reason"] = error_msg
                sys.exit(1)
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
            
            # 실패 시에도 리포트를 GitHub에 푸시하기 위해 push_to_github 호출
            if not DRY_RUN:
                from publish import push_to_github
                push_to_github("Update diagnostic automation report")
