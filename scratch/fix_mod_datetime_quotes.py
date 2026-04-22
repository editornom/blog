import os
import re

root_dir = r"src\data\blog"

def fix_mod_datetime(content):
    # Match 'modDatetime: "YYYY-MM-DD..."' or 'modDatetime: 'YYYY-MM-DD...''
    pattern = r'(modDatetime:\s*)([\'"])(.*?)\2'
    if re.search(pattern, content):
        new_content = re.sub(pattern, r'\1\3', content)
        return new_content
    return content

count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = fix_mod_datetime(content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed: {path}")
                count += 1

print(f"Total files fixed: {count}")
