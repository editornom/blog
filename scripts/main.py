import os
import sys
import uuid
import re
import time
import datetime
from dotenv import load_dotenv

from crawler import fetch_content
from generator import generate_blog_post
from reviewer import review_manuscript
from imagen_helper import generate_image
from translator import translate_and_save, translate_text
from publish import push_to_github
from accordian import load_faq_content, append_faq_to_draft
from headline_crawler import generate_daily_headlines_file
from trend_catcher import get_daily_topic_from_file
from search_expert import deep_search_and_filter
from faq_expert import generate_faq


load_dotenv()

if sys.platform == "win32":
    # Ensure terminal can handle UTF-8/Emojis on Windows
    sys.stdout.reconfigure(encoding='utf-8')

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

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
        lines.append(f"- 🖼️ 이미지 생성: ✅ {report['images']['success']} / {report['images']['requested']} 완료")
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
        "draft": {"success": None, "path": None},
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
            # First, strip existing FAQ if any to avoid duplicates
            if "## ✅ 자주 묻는 질문 (FAQ)" in draft:
                draft = draft.split("## ✅ 자주 묻는 질문 (FAQ)")[0].strip()
            
            draft = append_faq_to_draft(draft, faqs)
            print(f"Added {len(faqs)} FAQ items to the draft.")
            
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
        "crawl": {"success": False, "count": 0, "error": None},
        "draft": {"success": False, "path": None},
        "detox": {"success": False, "error": None},
        "images": {"success": 0, "requested": 0},
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

    # 3. Generate initial draft
    combined_body = "\n\n---\n\n".join([c['body'] for c in all_content])
    print(f"\n=== Combined {len(all_content)} pages into {len(combined_body)} chars ===")
    
    print(f"Generating draft with Gemini ({folder} mode)...")
    crawled_summary = {
        "title": all_content[0].get('title', 'Untitled Issue'),
        "url": urls[0],
        "body": combined_body[:30000] # Limit to avoid token issues
    }
    
    draft = generate_blog_post(crawled_summary, folder=folder)
    if not draft:
        print("Error: Failed to generate initial blog post.")
        print_final_briefing(report)
        return
    
    # 3.5 Stage 3.5: Manuscript Inspection (Detox)
    print(f"\n=== Stage 3.5: Manuscript Inspection (Detox) ===")
    reviewed_draft = review_manuscript(draft, folder=folder)
    if reviewed_draft:
        draft = reviewed_draft
        report["detox"]["success"] = True
    else:
        report["detox"]["error"] = "Detox failed, keeping original draft"

    # 3.7 Add FAQ if requested
    if include_faq and keyword:
        # 🚀 [New Pipeline] Generate FAQ automatically before loading
        generate_faq(draft, keyword)
        
        faqs = load_faq_content(keyword)
        if faqs:
            draft = append_faq_to_draft(draft, faqs)
            print(f"Added {len(faqs)} FAQ items to the draft.")
        else:
            print(f"Warning: FAQ file not found or empty for keyword '{keyword}'")

    # 4. Process Images (Regex to find [이미지: ...])
    image_placeholders = re.findall(r'\[이미지: (.*?)\]', draft)
    
    # Define source image directory based on keyword (Sanitize for Windows paths)
    source_folder_name = keyword if keyword else "general"
    # 윈도우에서 사용할 수 없는 특수문자 제거 (: / \ ? * < > | ")
    source_folder_name = re.sub(r'[\s\\/:*?"<>|]+', '_', source_folder_name).strip('_')
    
    source_img_dir = os.path.join("source", folder, source_folder_name)
    os.makedirs(source_img_dir, exist_ok=True)
    
    print(f"Found {len(image_placeholders)} image placeholders.")
    report["images"]["requested"] = len(image_placeholders)

    for i, prompt in enumerate(image_placeholders):
        img_uuid = str(uuid.uuid4())[:8]
        img_filename = f"{img_uuid}-{i}.png"
        img_path = os.path.join(source_img_dir, img_filename)
        
        print(f"Generating AI image for: {prompt[:50]}...")
        generated_path = generate_image(prompt, img_path)
        
        # Rate limit
        print("Waiting 20 seconds to respect API rate limits...")
        time.sleep(20) 
        
        if generated_path:
            report["images"]["success"] += 1
            rel_path = f"../../../../../source/{folder}/{source_folder_name}/{img_filename}"
            
            # Translate English prompt to Korean for Alt Tag
            translated_alt = translate_text(prompt, "ko")
            md_img_link = f"![{translated_alt}]({rel_path})"
            
            draft = draft.replace(f"[이미지: {prompt}]", md_img_link)
            
            if i == 0:
                draft = re.sub(r'ogImage: ".*?"', f'ogImage: "{rel_path}"', draft)

    # 5. Save the Final Markdown File
    slug_match = re.search(r'slug: "(.*?)"', draft)
    slug = slug_match.group(1) if slug_match else f"post-{datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
    
    target_dir = os.path.join("src", "data", "blog", "ko", folder)
    os.makedirs(target_dir, exist_ok=True)
    post_path = os.path.join(target_dir, f"{slug}.md")
    
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(draft)
    
    print(f"\n[DONE] Successfully saved Korean blog post to {post_path}!")
    report["draft"]["success"] = True
    report["draft"]["path"] = post_path
    
    # 6. Translate to EN, CN, JP (Skip if folder is haionnet)
    if folder == "haionnet":
        print(f"\n=== Skipping translation for 'haionnet' folder (Korea-only service) ===")
    else:
        print(f"\n=== Translating to 3 languages ===")
        results = translate_and_save(draft, slug, folder)
        report["translations"] = results
    
    # 7. Push to GitHub
    if DRY_RUN:
        print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
    else:
        # 무인 자동화를 위해 질문 없이 바로 진행 (y로 간주)
        print(f"\n🚀 모든 작업 완료. '{slug}' 포스트를 GitHub에 자동으로 연동(Push)합니다.")
        push_to_github(f"Auto-generate post: {slug}")
        
    # 🚨 FINAL BRIEFING
    print_final_briefing(report)

if __name__ == "__main__":
    # Usage 1 (Full): python main.py [keyword] [folder]
    # Usage 2 (Retry): python main.py [path_to_korean.md] [folder] [target_lang]
    input_arg = sys.argv[1] if len(sys.argv) > 1 else None
    folder = sys.argv[2] if len(sys.argv) > 2 else "posts"
    target_lang = sys.argv[3] if len(sys.argv) > 3 else None
    
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
            process_urls(urls=top_urls, keyword=input_arg, folder=folder, include_faq=include_faq)
        else:
            print(f"❌ '{input_arg}'에 대한 검색 결과에서 유효한 소스를 찾지 못했습니다.")
    else:
        # 🔥 완전 자동 모드 (파일 생성 -> 분석 -> 포스팅)
        print("\n🚀 [AUTO MODE] No arguments provided. Starting full automation pipeline...")
        
        # 1. 크롤러 실행: list.txt 읽어서 20260410.txt 생성
        daily_file = generate_daily_headlines_file("list.txt")
        
        if daily_file:
            # 2. 트렌드 캐처 실행: 수집된 파일 읽어서 키워드 도출 및 URL 파일 생성
            auto_keyword = get_daily_topic_from_file(daily_file)
            
            if auto_keyword:
                print(f"✨ Auto-selected Keyword: {auto_keyword}")
                
                # 🚀 [New Pipeline] DeepSearch & Filter
                top_urls = deep_search_and_filter(auto_keyword, num_results=100)
                
                if top_urls:
                    # 3. 선별된 고품질 URL들을 사용하여 포스팅 작성
                    process_urls(urls=top_urls, keyword=auto_keyword, folder=folder, include_faq=include_faq)
                else:
                    print("❌ 검색 결과에서 유효한 소스를 찾지 못했습니다.")
            else:
                print("❌ AI 키워드 선정에 실패했습니다.")
        else:
            print("❌ 헤드라인 수집에 실패하여 파이프라인을 중단합니다.")
