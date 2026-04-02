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

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

def process_urls(urls_file="urls.txt", target_url=None):
    """
    Main orchestration function to process multiple URLs into blog posts.
    """
    if target_url:
        urls = [target_url]
    elif not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found.")
        return
    else:
        with open(urls_file, "r") as f:
            # Filter out comments and category headers
            urls = [line.strip() for line in f if line.strip() and line.strip().startswith("http")]

    if not urls:
        print(f"No valid URLs found in {urls_file or 'argument'}.")
        return

    for url in urls:
        print(f"\n--- Processing: {url} ---")
        
        # 1. Fetch Content
        content = fetch_content(url)
        if not content:
            continue
            
        # 2. Generate Draft with Gemini
        print("Generating draft with Gemini...")
        draft = generate_blog_post(content)
        if not draft:
            continue
            
        # 3. Process Images (Regex to find [이미지: ...])
        # Find all [이미지: ...] patterns
        image_placeholders = re.findall(r'\[이미지: (.*?)\]', draft)
        
        print(f"Found {len(image_placeholders)} image placeholders.")
        
        # Mapping to replace placeholders with real paths
        for i, prompt in enumerate(image_placeholders):
            # Generate a unique filename
            img_uuid = str(uuid.uuid4())[:8]
            img_filename = f"post-img-{img_uuid}-{i}.png"
            img_path = os.path.join("src", "assets", "images", img_filename)
            
            # Call Imagen API
            print(f"Generating AI image for: {prompt[:50]}...")
            generated_path = generate_image(prompt, img_path)
            
            # Rate limiting: wait between image generations (API is called even in dry run)
            print("Waiting 20 seconds to respect API rate limits...")
            time.sleep(20) 
            
            if generated_path:
                # Replace the entire placeholder with Markdown image syntax (relative path)
                md_img_link = f"![AI Generated Image](../../assets/images/{img_filename})"
                draft = draft.replace(f"[이미지: {prompt}]", md_img_link)
                
                # Update ogImage placeholder in frontmatter if it's the first image
                if i == 0:
                    draft = re.sub(r'ogImage: ".*?"', f'ogImage: "../../assets/images/{img_filename}"', draft)

        # 4. Save the Final Markdown File
        # Extract slug from frontmatter using regex or simple search
        slug_match = re.search(r'slug: "(.*?)"', draft)
        slug = slug_match.group(1) if slug_match else f"post-{datetime.date.today()}-{uuid.uuid4().hex[:6]}"
        
        post_filename = f"{slug}.md"
        post_path = os.path.join("src", "data", "blog", post_filename)
        
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(draft)
        
        print(f"Successfully saved blog post to {post_path}!")
        
        # 5. Push to GitHub
        if DRY_RUN:
            print(f"Dry run enabled. Skipping push to GitHub for {slug}.")
        else:
            push_to_github(f"feat: add automated blog post for {slug}")

if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else "urls.txt"
    
    # Intelligently decide whether to treat as single URL or a file
    if arg.startswith("http"):
        print(f"Targeting single URL: {arg}")
        process_urls(target_url=arg)
    elif arg.endswith(".txt"):
        print(f"Targeting specialized URL file: {arg}")
        process_urls(urls_file=arg)
    else:
        # Fallback to default urls.txt if no valid arg
        print(f"No specific target provided. Defaulting to: {arg}")
        process_urls(urls_file=arg)
