import glob
import re

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        txt = f.read()
    parts = txt.split("---", 2)
    if len(parts) >= 3:
        fm = parts[1]
        fm = re.sub(r'^(\s*(?:-\s*q:|a:)\s+)(?![("\'])(.*)$', 
                    lambda m: m.group(1) + '"' + m.group(2).replace('"', "'") + '"', 
                    fm, flags=re.MULTILINE)
        new_txt = f"---{fm}---{parts[2]}"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_txt)
            print(f"Fixed {filepath}")

for path in glob.glob("src/data/blog/*/posts/260428_*.md"):
    fix_file(path)
