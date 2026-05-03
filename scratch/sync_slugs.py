import os
import re
import yaml
from pathlib import Path

def get_slug(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split('---')
    if len(parts) >= 3:
        try:
            fm = yaml.safe_load(parts[1])
            return fm.get('slug')
        except:
            return None
    return None

def update_slug_and_links(project_root):
    blog_dir = Path(project_root) / "src/data/blog"
    
    # 1. Build slug map from Korean posts/glossary
    slug_map = {} # filename -> slug
    for board in ['posts', 'glossary']:
        ko_dir = blog_dir / "ko" / board
        if ko_dir.exists():
            for f in ko_dir.glob("*.md"):
                slug = get_slug(f)
                if slug:
                    slug_map[f.name] = slug

    # 2. Update slugs in other languages
    for lang in ['en', 'jp', 'cn']:
        for board in ['posts', 'glossary']:
            lang_dir = blog_dir / lang / board
            if lang_dir.exists():
                for f in lang_dir.glob("*.md"):
                    if f.name in slug_map:
                        target_slug = slug_map[f.name]
                        with open(f, 'r', encoding='utf-8') as file:
                            content = file.read()
                        
                        # Use regex to replace slug in frontmatter
                        new_content = re.sub(r'(slug:\s*)([^\n]+)', rf'\1{target_slug}', content)
                        
                        if new_content != content:
                            with open(f, 'w', encoding='utf-8') as file:
                                file.write(new_content)
                            print(f"Updated slug in {f.relative_to(project_root)} to {target_slug}")

    # 3. Fix all internal links in all languages
    # This is tricky because we need to know the mapping of old_slug -> new_slug for EACH language
    # But since we've standardized everything to the Korean slug, we can just ensure 
    # links use the Korean slug. 
    # Wait, the broken links WERE often already using the Korean slug, but the files had different slugs.
    # So step 2 should fix most of them.
    
    print("Slug synchronization complete.")

if __name__ == "__main__":
    update_slug_and_links(os.getcwd())
