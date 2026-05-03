import os
import re
from pathlib import Path

def revert_paths(base_path):
    md_files = list(Path(base_path).rglob("*.md"))
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Revert 4 levels back to 5 levels
        new_content = content.replace('../../../../source/', '../../../../../source/')
        
        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Reverted paths in {md_file}")

if __name__ == "__main__":
    blog_dir = "src/data/blog"
    revert_paths(blog_dir)
