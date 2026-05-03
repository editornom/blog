import os
import re
import yaml
import urllib.parse
from pathlib import Path

def check_posts(base_path, project_root):
    md_files = list(Path(base_path).rglob("*.md"))
    results = []
    
    # Regex for images in markdown: ![alt](path)
    img_regex = re.compile(r'!\[.*?\]\((.*?)\)')
    
    for md_file in md_files:
        errors = []
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Check Frontmatter
        parts = content.split('---')
        if len(parts) < 3:
            errors.append("Missing frontmatter delimiter")
        else:
            try:
                fm = yaml.safe_load(parts[1])
                required = ['title', 'slug', 'description', 'pubDatetime']
                for field in required:
                    if field not in fm or not fm[field]:
                        errors.append(f"Missing required field: {field}")
                
                if 'ogImage' in fm and fm['ogImage']:
                    og_img = fm['ogImage']
                    if isinstance(og_img, str) and not og_img.startswith('http') and not og_img.startswith('/'):
                        # Decode path in case it's encoded in frontmatter (though rare)
                        decoded_img = urllib.parse.unquote(og_img)
                        img_path = md_file.parent / decoded_img
                        if not img_path.exists():
                            errors.append(f"Broken ogImage: {og_img}")
            except Exception as e:
                errors.append(f"Invalid YAML: {str(e)}")
        
        # 2. Check Images in body
        images = img_regex.findall(content)
        for img in images:
            if not img.startswith('http') and not img.startswith('/'):
                # Decode URL encoded path (e.g., %28 -> ()
                decoded_img = urllib.parse.unquote(img)
                img_path = md_file.parent / decoded_img
                if not img_path.exists():
                    errors.append(f"Broken body image: {img} (Decoded: {decoded_img})")
            elif img.startswith('/'):
                public_img_path = Path(project_root) / "public" / img.lstrip('/')
                if not public_img_path.exists():
                    errors.append(f"Broken body image (public): {img}")

        if errors:
            results.append({
                "file": str(md_file.relative_to(project_root)),
                "errors": errors
            })
            
    return results

if __name__ == "__main__":
    project_root = os.getcwd()
    blog_dir = os.path.join(project_root, "src/data/blog")
    findings = check_posts(blog_dir, project_root)
    if not findings:
        print("All posts are clean!")
    else:
        print(f"Found issues in {len(findings)} files:")
        for item in findings:
            print(f"File: {item['file']}")
            for err in item['errors']:
                print(f"  - {err}")
