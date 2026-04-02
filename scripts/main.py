import os
import re
import uuid
import datetime
import time
from dotenv import load_dotenv
from crawler import fetch_content
from generator import generate_blog_post
from imagen_helper import generate_image
from publish import push_to_github
from translator import translate_and_save

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

def process_urls(urls_file="urls.txt", target_url=None, folder="posts"):
    """
    Main orchestration function.
    - If target_url: process a single URL into one post.
    - If urls_file: crawl ALL URLs in the file, combine them, and generate ONE post.
    
    Args:
        urls_file: Path to a text file containing URLs (one per line).
        target_url: A single URL to process directly.
        folder: Target folder — either 'posts' or 'haionnet'.
    """
    if folder not in ("posts", "haionnet"):
        print(f"Error: Invalid folder '{folder}'. Must be 'posts' or 'haionnet'.")
        return

    if target_url:
        urls = [target_url]
    elif not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found.")
        return
    else:
        with open(urls_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Extract all URLs from the file (find http links anywhere in the line)
        urls = []
        for line in lines:
            found = re.findall(r'(https?://\S+)', line)
            urls.extend(found)

    if not urls:
        print(f"No valid URLs found.")
        return

    print(f"\n=== Found {len(urls)} URLs to crawl ===")
    print(f"Category: {folder}")

    # 1. Crawl ALL URLs and combine content
    all_content = []
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Crawling: {url}")
        content = fetch_content(url)
        if content and content['body']:
            all_content.append(content)
            print(f"  ✓ Got {len(content['body'])} chars")
        else:
            print(f"  ✗ Skipped (no content)")

    if not all_content:
        print("Error: No content could be fetched from any URL.")
        return

    # 2. Merge all crawled content into one combined context
    combined_body = ""
    for c in all_content:
        combined_body += f"\n\n--- 출처: {c['url']} ---\n제목: {c['title']}\n{c['body']}\n"

    combined_content = {
        "title": all_content[0]['title'],  # Use first page's title as base
        "url": urls[0],
        "body": combined_body
    }

    print(f"\n=== Combined {len(all_content)} pages into {len(combined_body)} chars ===")

    # 3. Generate ONE draft with Gemini
    print(f"Generating draft with Gemini ({folder} mode)...")
    draft = generate_blog_post(combined_content, folder=folder)
    if not draft:
        print("Error: Failed to generate blog post.")
        return
        
    # 4. Process Images (Regex to find [이미지: ...])
    image_placeholders = re.findall(r'\[이미지: (.*?)\]', draft)
    
    print(f"Found {len(image_placeholders)} image placeholders.")
    
    for i, prompt in enumerate(image_placeholders):
        img_uuid = str(uuid.uuid4())[:8]
        img_filename = f"post-img-{img_uuid}-{i}.png"
        img_path = os.path.join("src", "assets", "images", img_filename)
        
        print(f"Generating AI image for: {prompt[:50]}...")
        generated_path = generate_image(prompt, img_path)
        
        print("Waiting 20 seconds to respect API rate limits...")
        time.sleep(20) 
        
        if generated_path:
            md_img_link = f"![AI Generated Image](../../../../assets/images/{img_filename})"
            draft = draft.replace(f"[이미지: {prompt}]", md_img_link)
            
            if i == 0:
                draft = re.sub(r'ogImage: ".*?"', f'ogImage: "../../../../assets/images/{img_filename}"', draft)

    # 5. Save the Final Markdown File
    slug_match = re.search(r'slug: "(.*?)"', draft)
    slug = slug_match.group(1) if slug_match else f"post-{datetime.date.today()}-{uuid.uuid4().hex[:6]}"
    
    post_filename = f"{slug}.md"
    post_dir = os.path.join("src", "data", "blog", "ko", folder)
    os.makedirs(post_dir, exist_ok=True)
    post_path = os.path.join(post_dir, post_filename)
    
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(draft)
    
    print(f"\n✓ Successfully saved Korean blog post to {post_path}!")
    
    # 6. Translate to EN, CN, JP
    print(f"\n=== Translating to 3 languages ===")
    translated_files = translate_and_save(draft, slug, folder)
    print(f"\n✓ Translated to {len(translated_files)} languages")
    
    # 7. Push to GitHub
    if DRY_RUN:
        print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
    else:
        push_to_github(f"feat: add automated blog post for {slug}")

if __name__ == "__main__":
    import sys
    
    # Usage: python main.py [URL or file] [posts|haionnet]
    arg = sys.argv[1] if len(sys.argv) > 1 else "urls.txt"
    folder = sys.argv[2] if len(sys.argv) > 2 else "posts"
    
    print(f"Category: {folder}")
    
    if arg.startswith("http"):
        print(f"Targeting single URL: {arg}")
        process_urls(target_url=arg, folder=folder)
    elif arg.endswith(".txt"):
        print(f"Targeting URL file: {arg}")
        process_urls(urls_file=arg, folder=folder)
    else:
        print(f"No specific target provided. Defaulting to: {arg}")
        process_urls(urls_file=arg, folder=folder)

