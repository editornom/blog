import os
import yaml
from pathlib import Path

def check_duplicates_and_quality(base_path):
    md_files = list(Path(base_path).rglob("*.md"))
    slugs = {}
    quality_issues = []
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        parts = content.split('---')
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                slug = fm.get('slug')
                lang = md_file.parent.parent.name # en, ko, jp, cn
                
                key = f"{lang}/{slug}"
                if key in slugs:
                    slugs[key].append(str(md_file))
                else:
                    slugs[key] = [str(md_file)]
                
                # Quality check
                body = parts[2].strip()
                if len(body) < 200:
                    quality_issues.append(f"Short content ({len(body)} chars): {md_file}")
                
                if not fm.get('faqs'):
                    # quality_issues.append(f"Missing FAQs: {md_file}")
                    pass
                
            except:
                pass
                
    duplicates = {k: v for k, v in slugs.items() if len(v) > 1}
    return duplicates, quality_issues

if __name__ == "__main__":
    blog_dir = "src/data/blog"
    dupes, quality = check_duplicates_and_quality(blog_dir)
    
    if dupes:
        print("Duplicate slugs found:")
        for k, v in dupes.items():
            print(f"  {k}: {v}")
    else:
        print("No duplicate slugs found.")
        
    if quality:
        print("Quality issues found:")
        for q in quality:
            print(f"  {q}")
    else:
        print("No quality issues found.")
