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
from translator import translate_and_save
from publish import push_to_github

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

def print_final_briefing(report):
    """
    Prints a clean, Korean summary of the entire execution process.
    """
    print("\n" + "="*40)
    print("📢 최종 발행 분석 보고서")
    print("="*40)
    
    # 1. Crawling
    if report["crawl"]["success"] is not None:
        if report["crawl"]["success"]:
            print(f"- 🔍 데이터 수집: ✅ 성공 ({report['crawl']['count']}개 URL)")
        else:
            print(f"- 🔍 데이터 수집: ❌ 실패 ({report['crawl']['error']})")
    else:
        print("- 🔍 데이터 수집: ⚪ 건너뜀 (파일 직접 입력 모드)")
        
    # 2. Draft & Detox
    if report["draft"]["success"] is not None:
        if report["draft"]["success"]:
            print(f"- 📑 원고 초안: ✅ 성공 ({report['draft']['path']})")
            if report["detox"]["success"]:
                print(f"- ✨ 원고 검수: ✅ 완료 (디톡스 필터 적용)")
            else:
                print(f"- ✨ 원고 검수: ⚠️ 건너뜀 또는 실패 ({report['detox']['error']})")
        else:
            print(f"- 📑 원고 초안: ❌ 실패")
    else:
        print("- 📑 원고 초안/검수: ⚪ 건너뜀 (기존 파일 사용)")

    # 3. Images
    if report["images"]["requested"] > 0:
        print(f"- 🖼️ 이미지 생성: ✅ {report['images']['success']} / {report['images']['requested']} 완료")
    elif report["images"]["success"] is None:
         print("- 🖼️ 이미지 생성: ⚪ 건너뜀")
    else:
        print("- 🖼️ 이미지 생성: ⚪ 없음 (플레이스홀더 미발견)")

    # 4. Translations
    print("- 🌐 다국어 번역 상태:")
    if not report["translations"]:
        print("  - (번역 단계가 실행되지 않았습니다)")
    else:
        for lang, res in report["translations"].items():
            status = "✅ 성공" if res["success"] else f"❌ 실패 (사유: {res['error']})"
            print(f"  - {lang.upper()}: {status}")

    print("="*40)
    if any(not res["success"] for res in report["translations"].values()):
        print("💡 실패한 번역이 있다면 API 부하일 가능성이 높습니다. 잠시 후 다시 시도해 보세요.")
    print("="*40 + "\n")

def process_single_file(file_path, folder="posts", target_lang=None):
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

    slug = os.path.splitext(os.path.basename(file_path))[0]
    
    # Run Translation
    print(f"\n=== Translating to requested languages ===")
    target_langs = [target_lang] if target_lang else None
    results = translate_and_save(draft, slug, folder, target_langs=target_langs)
    report["translations"] = results

    # Optional Push
    if DRY_RUN:
        print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
    else:
        push_to_github(f"Re-translate post: {slug} ({target_lang if target_lang else 'all'})")

    print_final_briefing(report)

def process_urls(keyword=None, folder="posts"):
    """
    Main pipeline: Crawl -> Generate -> Review -> Image Gen -> Translate -> (Push)
    """
    report = {
        "crawl": {"success": False, "count": 0, "error": None},
        "draft": {"success": False, "path": None},
        "detox": {"success": False, "error": None},
        "images": {"success": 0, "requested": 0},
        "translations": {}
    }

    # 1. Determine URL source
    if keyword:
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

    # 4. Process Images (Regex to find [이미지: ...])
    image_placeholders = re.findall(r'\[이미지: (.*?)\]', draft)
    
    # Define source image directory based on keyword
    source_folder_name = keyword if keyword else "general"
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
            md_img_link = f"![AI Generated Image]({rel_path})"
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
    
    # 6. Translate to EN, CN, JP
    print(f"\n=== Translating to 3 languages ===")
    results = translate_and_save(draft, slug, folder)
    report["translations"] = results
    
    # 7. Push to GitHub
    if DRY_RUN:
        print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
    else:
        push_to_github(f"Auto-generate post: {slug}")
        
    # 🚨 FINAL BRIEFING
    print_final_briefing(report)

if __name__ == "__main__":
    # Usage 1 (Full): python main.py [keyword] [folder]
    # Usage 2 (Retry): python main.py [path_to_korean.md] [folder] [target_lang]
    input_arg = sys.argv[1] if len(sys.argv) > 1 else None
    folder = sys.argv[2] if len(sys.argv) > 2 else "posts"
    target_lang = sys.argv[3] if len(sys.argv) > 3 else None
    
    if input_arg and input_arg.endswith(".md"):
        process_single_file(input_arg, folder, target_lang)
    else:
        process_urls(keyword=input_arg, folder=folder)
