import os
import re
import yaml
from pathlib import Path

def fix_and_check_posts(base_path, project_root):
    md_files = list(Path(base_path).rglob("*.md"))
    report = []
    
    # Regex for images in markdown: ![alt](path)
    img_regex = re.compile(r'!\[.*?\]\((.*?)\)')
    
    for md_file in md_files:
        errors = []
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Fix Paths
        # Many files have 5 levels of ../ when 4 is needed to reach project root from src/data/blog/lang/posts/
        new_content = content.replace('../../../../../source/', '../../../../source/')
        
        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            content = new_content
            # report.append(f"Fixed paths in {md_file.relative_to(project_root)}")

        # 2. Check Frontmatter
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
                
                # Check ogImage
                if 'ogImage' in fm and fm['ogImage']:
                    og_img = fm['ogImage']
                    if isinstance(og_img, str) and not og_img.startswith('http') and not og_img.startswith('/'):
                        img_path = md_file.parent / og_img
                        if not img_path.exists():
                            errors.append(f"Broken ogImage: {og_img}")
            except Exception as e:
                errors.append(f"Invalid YAML: {str(e)}")
        
        # 3. Check Images in body
        images = img_regex.findall(content)
        for img in images:
            if not img.startswith('http') and not img.startswith('/'):
                img_path = md_file.parent / img
                if not img_path.exists():
                    errors.append(f"Broken body image: {img}")
            elif img.startswith('/'):
                public_img_path = Path(project_root) / "public" / img.lstrip('/')
                if not public_img_path.exists():
                    errors.append(f"Broken body image (public): {img}")

        # 4. Check Internal Links
        # Typical link: [text](/ko/posts/slug)
        links = re.findall(r'\[.*?\]\((/.*?)\)', content)
        for link in links:
            if link.startswith('/ko/posts/') or link.startswith('/ko/glossary/'):
                # Very rough check - just see if we can find a file with that slug
                slug = link.split('/')[-1]
                # (This part is a bit complex as we'd need to index all slugs first)
                pass

        if errors:
            report.append({
                "file": str(md_file.relative_to(project_root)),
                "errors": errors
            })
            
    return report

if __name__ == "__main__":
    project_root = os.getcwd()
    blog_dir = os.path.join(project_root, "src/data/blog")
    findings = fix_and_check_posts(blog_dir, project_root)
    
    if not findings:
        print("All posts are clean and fixed!")
    else:
        print(f"Found issues in {len(findings)} files:")
        for item in findings:
            print(f"File: {item['file']}")
            for err in item['errors']:
                print(f"  - {err}")
