import os
from pathlib import Path

def fix_leading_spaces():
    blog_dir = Path("src/data/blog")
    md_files = list(blog_dir.rglob("*.md"))
    fixed_count = 0
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.splitlines(keepends=True)
        modified = False
        new_lines = []
        for line in lines:
            # If line starts with spaces and has ![, let's strip leading spaces
            stripped = line.lstrip()
            if stripped.startswith("![") and line != stripped:
                new_lines.append(stripped)
                modified = True
            else:
                new_lines.append(line)
        
        if modified:
            with open(md_file, "w", encoding="utf-8", newline="") as f:
                f.writelines(new_lines)
            print(f"Fixed leading spaces in {md_file}")
            fixed_count += 1
            
    print(f"Finished. Fixed {fixed_count} files.")

if __name__ == "__main__":
    fix_leading_spaces()
