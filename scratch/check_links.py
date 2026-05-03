import os
import re
import yaml
from pathlib import Path

def check_internal_links(base_path, project_root):
    md_files = list(Path(base_path).rglob("*.md"))
    
    # Index all existing slugs by language and type (posts or glossary)
    valid_paths = set()
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            parts = content.split('---')
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1])
                slug = fm.get('slug')
                lang = md_file.parent.parent.name
                board = md_file.parent.name # posts or glossary
                valid_paths.add(f"/{lang}/{board}/{slug}")
        except:
            pass

    link_errors = []
    # Regex for internal links: [text](/lang/board/slug)
    link_regex = re.compile(r'\[.*?\]\((/.*?)\)')
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = link_regex.findall(content)
        for link in links:
            # Only check links that start with one of the languages
            if any(link.startswith(f"/{l}/") for l in ['ko', 'en', 'jp', 'cn']):
                # Remove trailing slash if any
                clean_link = link.rstrip('/')
                if clean_link not in valid_paths:
                    # Special case: some links might be to /ko/posts/pagename which is same as slug
                    if clean_link not in valid_paths:
                        link_errors.append(f"Broken link in {md_file.relative_to(project_root)}: {link}")

    return link_errors

if __name__ == "__main__":
    project_root = os.getcwd()
    blog_dir = os.path.join(project_root, "src/data/blog")
    errors = check_internal_links(blog_dir, project_root)
    
    if not errors:
        print("All internal links are valid!")
    else:
        print(f"Found {len(errors)} broken internal links:")
        for err in errors:
            print(f"  - {err}")
