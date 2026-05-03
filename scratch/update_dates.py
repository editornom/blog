import os
import glob
import re
from datetime import datetime

# The new target dates
new_dates = [
    ("2026-04-25 09:00:00+09:00", "260425_"),
    ("2026-04-25 15:00:00+09:00", "260425_"),
    ("2026-04-26 09:00:00+09:00", "260426_"),
    ("2026-04-26 15:00:00+09:00", "260426_"),
    ("2026-04-27 09:00:00+09:00", "260427_"),
    ("2026-04-27 15:00:00+09:00", "260427_"),
    ("2026-04-28 09:00:00+09:00", "260428_")
]

langs = ['ko', 'en', 'jp', 'cn']
base_dir = "src/data/blog"

def get_pub_datetime(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'pubDatetime:\s*(.*)', content)
        if match:
            # We just parse it as string for sorting, assuming standard ISO format or similar
            return match.group(1).strip()
    return ""

ko_posts_dir = os.path.join(base_dir, 'ko', 'posts')
all_ko_posts = glob.glob(os.path.join(ko_posts_dir, "*.md"))

# Sort by pubDatetime
all_ko_posts.sort(key=get_pub_datetime)

for i, ko_post_path in enumerate(all_ko_posts):
    if i >= len(new_dates):
        break
    
    new_date_str, new_prefix = new_dates[i]
    old_filename = os.path.basename(ko_post_path)
    
    # Extract slug from filename (assuming YYMMDD_slug.md)
    slug = old_filename.split('_', 1)[1] if '_' in old_filename else old_filename
    new_filename = new_prefix + slug
    
    for lang in langs:
        old_path = os.path.join(base_dir, lang, 'posts', old_filename)
        new_path = os.path.join(base_dir, lang, 'posts', new_filename)
        
        if os.path.exists(old_path):
            with open(old_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update pubDatetime
            content = re.sub(r'pubDatetime:.*', f'pubDatetime: {new_date_str}', content)
            
            # Write back
            with open(old_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Rename file if prefix changed
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"[{lang}] Updated and renamed {old_filename} -> {new_filename}")
            else:
                print(f"[{lang}] Updated {old_filename}")
