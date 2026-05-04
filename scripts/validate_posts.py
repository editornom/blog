import os
import re
import yaml
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
import urllib.parse

def check_posts(base_path, days=1):
    project_root = Path(os.getcwd())
    blog_dir = project_root / "src/data/blog"
    source_dir = project_root / "source"
    
    now = datetime.now(timezone(timedelta(hours=9))) # KST
    threshold = now - timedelta(days=days)
    
    md_files = list(blog_dir.rglob("*.md"))
    
    slugs = {}
    valid_paths = set()
    errors = []
    
    # 1. First pass: Collect all slugs and valid paths
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            parts = content.split('---')
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1])
                slug = fm.get('slug')
                lang = md_file.parent.parent.name
                board = md_file.parent.name
                pub_date_str = fm.get('pubDatetime')
                
                # Check if it's within the time range
                if isinstance(pub_date_str, datetime):
                    pub_date = pub_date_str
                else:
                    try:
                        pub_date = datetime.fromisoformat(str(pub_date_str).replace('Z', '+00:00'))
                    except:
                        pub_date = None
                
                if pub_date and pub_date >= threshold:
                    # This post needs full check
                    pass
                else:
                    # Not in range, but we still need its slug for link checking
                    valid_paths.add(f"/{lang}/{board}/{slug}")
                    continue
                
                valid_paths.add(f"/{lang}/{board}/{slug}")
                
                # Duplicate slug check
                key = f"{lang}/{slug}"
                if key in slugs:
                    slugs[key].append(str(md_file))
                else:
                    slugs[key] = [str(md_file)]
                
                # 2. Integrity checks
                body = parts[2]
                
                # Placeholder check
                placeholders = re.findall(r'\[(이미지|Image|画像|图片):.*?\]', body)
                if placeholders:
                    errors.append(f"[{md_file.name}] Found {len(placeholders)} image placeholders.")

                # Image path check
                # Pattern: ![alt](path)
                images = re.findall(r'!\[.*?\]\((.*?)\)', body)
                og_image = fm.get('ogImage')
                if og_image:
                    images.append(og_image)
                
                for img_path in images:
                    if img_path.startswith('http'): continue
                    
                    # Resolve relative path
                    # Standard is ../../../../../source/posts/Folder/file.webp
                    # Current file is in src/data/blog/{lang}/{board}/{file}.md
                    # So 5 levels of ../ takes us to project root.
                    
                    normalized_path = img_path.replace('\\', '/')
                    if not normalized_path.startswith('../../../../../source/'):
                        # Special case for assets folder if it exists
                        if not normalized_path.startswith('../../../../assets/'):
                            errors.append(f"[{md_file.name}] Invalid image path prefix: {img_path}")
                            continue
                    
                    # Check if file exists
                    if 'source/' in normalized_path:
                        rel_path = normalized_path.split('source/')[1]
                        abs_img_path = source_dir / rel_path
                    elif 'assets/' in normalized_path:
                        rel_path = normalized_path.split('assets/')[1]
                        abs_img_path = project_root / "src/assets" / rel_path
                    else:
                        errors.append(f"[{md_file.name}] Invalid image path structure: {img_path}")
                        continue
                    
                    # URL decode
                    rel_path = urllib.parse.unquote(str(abs_img_path))
                    abs_img_path = Path(rel_path)
                    
                    if not abs_img_path.exists():
                        errors.append(f"[{md_file.name}] Broken image: {img_path}")

                # Internal link check
                links = re.findall(r'\[.*?\]\((/.*?)\)', body)
                for link in links:
                    if any(link.startswith(f"/{l}/") for l in ['ko', 'en', 'jp', 'cn']):
                        clean_link = link.split('#')[0].rstrip('/')
                        # We'll verify this in a second pass
                        pass
        except Exception as e:
            errors.append(f"[{md_file.name}] Frontmatter error: {e}")

    # 3. Duplicate check report
    for k, v in slugs.items():
        if len(v) > 1:
            errors.append(f"Duplicate slug '{k}' found in: {v}")

    # 4. Final link validation (Second pass)
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            parts = content.split('---')
            if len(parts) < 3: continue
            fm = yaml.safe_load(parts[1])
            pub_date_str = fm.get('pubDatetime')
            if isinstance(pub_date_str, datetime):
                pub_date = pub_date_str
            else:
                try:
                    pub_date = datetime.fromisoformat(str(pub_date_str).replace('Z', '+00:00'))
                except:
                    pub_date = None
            
            if not pub_date or pub_date < threshold: continue
            
            links = re.findall(r'\[.*?\]\((/.*?)\)', parts[2])
            for link in links:
                if any(link.startswith(f"/{l}/") for l in ['ko', 'en', 'jp', 'cn']):
                    clean_link = link.split('#')[0].rstrip('/')
                    if clean_link not in valid_paths:
                        errors.append(f"[{md_file.name}] Broken internal link: {link}")
        except:
            pass

    return errors

if __name__ == "__main__":
    days = 1
    if len(sys.argv) > 1:
        days = int(sys.argv[1])
    
    print(f"Auditing posts from the last {days} days...")
    errors = check_posts(".", days=days)
    
    if errors:
        print(f"\n--- Found {len(errors)} issues ---")
        for err in errors:
            print(f"ERR: {err}")
        sys.exit(1)
    else:
        print("\nAll clear! No issues found.")
        sys.exit(0)
